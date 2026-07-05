#!/usr/bin/env python3
import copy
import html
import json
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

PROJECT = Path("/Users/jackgreenberg/Desktop/rank-and-rent/David/clones/extremebuildouts.com")
PUBLIC = PROJECT / "public"
MEDIA_JSON = PUBLIC / "ours/projects/project-media.json"
DOMAIN = "https://extremebuildouts.com"
BIZ = "Extreme Buildouts LLC"

DETAIL_ROUTE = "/projects/mechanical-room-buildout"
INDEX_ROUTE = "/projects"
DETAIL_TITLE = "Commercial Mechanical Room Buildout"
INDEX_TITLE = "Example Projects"
DESCRIPTION = (
    "Example project photos from Extreme Buildouts LLC showing commercial mechanical room, "
    "A/C piping, plumbing, equipment, ductwork, and field buildout coordination."
)


def soupify(markup):
    return BeautifulSoup(markup, "html.parser")


def read_soup(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def write_soup(path, soup):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(soup), encoding="utf-8")


def set_text(el, text):
    if el is not None:
        el.clear()
        el.append(NavigableString(text))


def set_meta(soup, title, desc, route):
    full = f"{title} | {BIZ}"
    if soup.title:
        soup.title.string = full
    url = f"{DOMAIN}{route}"
    for attr, key, value in (
        ("name", "description", desc),
        ("property", "og:title", full),
        ("property", "og:description", desc),
        ("property", "og:url", url),
        ("name", "twitter:title", full),
        ("name", "twitter:description", desc),
    ):
        hits = soup.find_all("meta", attrs={attr: key})
        if not hits and soup.head:
            tag = soup.new_tag("meta")
            tag[attr] = key
            soup.head.append(tag)
            hits = [tag]
        for i, tag in enumerate(hits):
            if i == 0:
                tag["content"] = value
            else:
                tag.decompose()
    can = soup.find("link", rel="canonical")
    if can is None and soup.head:
        can = soup.new_tag("link", rel="canonical")
        soup.head.append(can)
    if can is not None:
        can["href"] = url
    html_tag = soup.find("html")
    if html_tag is not None:
        html_tag["data-wf-domain"] = "extremebuildouts.com"
        html_tag["data-wf-item-slug"] = route.strip("/") or "home"


PROJECT_CSS = """
<style id="rr-project-gallery-css">
.rr-project-teaser{background:#fff}
.rr-project-eyebrow{color:#009b67!important;text-transform:uppercase!important;letter-spacing:.12em!important;font-weight:800!important}
.rr-project-index-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;margin:34px 0}
.rr-project-index-card{display:block!important;background:#fff!important;border:1px solid rgba(69,85,102,.18)!important;text-decoration:none!important;color:inherit!important;box-shadow:0 10px 28px rgba(20,34,48,.07)!important}
.rr-project-index-card img{display:block!important;width:100%!important;height:320px!important;object-fit:cover!important}
.rr-project-index-card .filter-cards{padding:24px!important}
.rr-project-gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:22px 0 34px}
.rr-project-gallery figure{margin:0;background:#fff;border:1px solid rgba(69,85,102,.18);box-shadow:0 8px 22px rgba(20,34,48,.06)}
.rr-project-gallery img{display:block;width:100%;height:250px;object-fit:cover}
.rr-project-gallery figcaption{padding:12px 14px;font-weight:700;color:#455666;line-height:1.3}
.rr-project-gallery.rr-field-gallery img{height:190px}
.rr-project-video{margin:24px 0 36px;background:#111}
.rr-project-video video{display:block;width:100%;max-height:620px;background:#111}
.rr-project-metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:20px 0 28px}
.rr-project-metrics div{border:1px solid rgba(69,85,102,.18);padding:16px 18px;background:#fff}
.rr-project-metrics strong{display:block;color:#009b67;font-size:24px;line-height:1}
.rr-project-metrics span{display:block;margin-top:6px;font-weight:700;color:#455666}
@media(max-width:800px){.rr-project-index-grid,.rr-project-gallery,.rr-project-metrics{grid-template-columns:1fr}.rr-project-index-card img,.rr-project-gallery img,.rr-project-gallery.rr-field-gallery img{height:auto}.rr-project-video video{max-height:none}}
</style>
"""


def ensure_project_css(soup):
    if soup.head and not soup.find(id="rr-project-gallery-css"):
        soup.head.append(soupify(PROJECT_CSS))


def make_link(soup, label, href):
    a = soup.new_tag("a")
    a["class"] = ["refresh-navlinks", "top", "w-dropdown-toggle"]
    a["href"] = href
    a.string = label
    return a


def add_projects_nav(soup):
    header = soup.find("header")
    if header is not None and not header.find("a", href=INDEX_ROUTE):
        about = header.find("a", href="/about")
        nav = header.select_one(".nav-menu-2")
        link = make_link(soup, "Projects", INDEX_ROUTE)
        if about is not None:
            about.insert_before(link)
        elif nav is not None:
            nav.append(link)

    drawer = soup.select_one("[data-rr-mobile]")
    if drawer is not None and not drawer.find("a", href=INDEX_ROUTE):
        link = soup.new_tag("a", href=INDEX_ROUTE)
        link["class"] = ["rr-m-link"]
        link.string = "Projects"
        about = drawer.find("a", href="/about")
        if about is not None:
            about.insert_before(link)
        else:
            drawer.append(link)

    footer = soup.find("footer")
    if footer is not None and not footer.find("a", href=INDEX_ROUTE):
        about = footer.find("a", href="/about")
        link = soup.new_tag("a", href=INDEX_ROUTE)
        link.string = "Projects"
        if about is not None:
            about.insert_before(link)


def gallery(items, captions, extra_class=""):
    out = [f'<div class="rr-project-gallery {extra_class}">']
    for i, item in enumerate(items):
        caption = captions[i % len(captions)]
        out.append(
            '<figure>'
            f'<img loading="lazy" src="{html.escape(item["src"], quote=True)}" alt="{html.escape(caption, quote=True)}"/>'
            f'<figcaption>{html.escape(caption)}</figcaption>'
            '</figure>'
        )
    out.append("</div>")
    return "".join(out)


def project_body(media):
    featured = [m for m in media if m["type"] == "chat-image"]
    field = [m for m in media if m["type"] == "email-image"]
    video = next((m for m in media if m["type"] == "video"), None)
    featured_captions = [
        "Piped mechanical controls and metering tied into the buildout scope.",
        "Insulated overhead pipe runs coordinated with equipment access.",
        "Mechanical room piping, supports, and service clearances in progress.",
        "Wide mechanical infrastructure view with ductwork and utility routing.",
        "Equipment room tank area during active construction and material staging.",
    ]
    field_captions = [
        "Ductwork and ceiling infrastructure progress.",
        "Field coordination for commercial interior systems.",
        "Mechanical equipment placement and service access.",
        "Overhead utilities coordinated before finish work.",
        "Rough-in and support work ahead of closeout.",
        "Exterior rooftop equipment and utility routing.",
    ]
    video_html = ""
    if video:
        poster = video.get("poster", featured[0]["src"] if featured else "")
        video_html = (
            '<h2>Walkthrough Video</h2>'
            '<p>Short field video from the same project media set, included so owners can see the kind of above-ceiling and equipment-room coordination that happens before a finished space is turned over.</p>'
            f'<div class="rr-project-video"><video controls preload="metadata" poster="{html.escape(poster, quote=True)}">'
            f'<source src="{html.escape(video["src"], quote=True)}" type="video/mp4"/>'
            "</video></div>"
        )
    return (
        '<h2>Mechanical Room Buildout Example</h2>'
        '<p>This example project shows the kind of field work Extreme Buildouts LLC coordinates when a commercial space needs A/C, plumbing, electrical, mechanical equipment, pipe routing, access, and finish planning handled together. The photos are jobsite examples, not stock images, and they show the practical details that decide whether a buildout works after turnover.</p>'
        '<p>The visible work includes overhead pipe runs, insulated mechanical lines, control panels, valves, meters, equipment pads, tank areas, service clearances, and utility routing. Those details have to be planned before ceilings close, finishes start, or the owner is left managing conflicts between trades.</p>'
        '<div class="rr-project-metrics"><div><strong>MEP</strong><span>A/C, plumbing, electrical, and controls</span></div><div><strong>Field</strong><span>Real project photos from active work</span></div><div><strong>Scope</strong><span>Mechanical room and utility coordination</span></div></div>'
        '<h2>Primary Project Photos</h2>'
        + gallery(featured, featured_captions)
        + video_html
        + '<h2>Additional Field Examples</h2>'
        '<p>The additional photos from the project emails show more commercial buildout conditions: ductwork, ceiling utilities, structural openings, rooftop equipment, rough-in work, lifts, equipment staging, and field coordination before finishes are complete.</p>'
        + gallery(field, field_captions, "rr-field-gallery")
        + '<h2>What This Shows Owners</h2>'
        '<p>Commercial buildouts are not just finish work. The finished space depends on what happens in mechanical rooms, above ceilings, behind walls, on rooftops, and around equipment clearances. Extreme Buildouts LLC uses that field reality to plan scopes before the project turns into disconnected trade visits.</p>'
        '<p>If a space needs A/C, electrical, plumbing, structural coordination, interior finish work, or ground-up planning, this is the kind of detail that should be reviewed early. The goal is a space that opens cleanly, works correctly, and does not leave the owner chasing unresolved trade gaps after construction.</p>'
        '<h2>Ready to plan the scope?</h2><a class="button underlined-text w-button" href="/contact">Request a Buildout Review</a>'
    )


def build_project_detail(media):
    base = read_soup(PUBLIC / "services/commercial-ac-buildouts.html")
    ensure_project_css(base)
    set_meta(base, DETAIL_TITLE, DESCRIPTION, DETAIL_ROUTE)
    for h in base.find_all("h1"):
        set_text(h, DETAIL_TITLE)
    rich = base.select_one(".paragraph.projects.w-richtext")
    if rich is not None:
        rich.clear()
        rich.append(soupify(project_body(media)))
    hero = None
    for col in base.select("section.padding > div.float-left"):
        if "projects-left-column" not in (col.get("class") or []):
            hero = col.find("img")
            break
    featured = next((m for m in media if m["type"] == "chat-image"), None)
    if hero is not None and featured is not None:
        hero["src"] = featured["src"]
        hero["alt"] = DETAIL_TITLE
        for attr in ("srcset", "data-src", "data-srcset"):
            hero.attrs.pop(attr, None)
    add_projects_nav(base)
    write_soup(PUBLIC / "projects/mechanical-room-buildout.html", base)


def build_projects_index(media):
    base = read_soup(PUBLIC / "services.html")
    ensure_project_css(base)
    set_meta(base, INDEX_TITLE, "Example project photos and videos from Extreme Buildouts LLC.", INDEX_ROUTE)
    main = base.select_one("body > .padding")
    featured = next((m for m in media if m["type"] == "chat-image"), None)
    email_images = [m for m in media if m["type"] == "email-image"]
    field = next((m for m in email_images if m["filename"].startswith("field-project-photo-22-")), None)
    field = field or next((m for m in email_images if m["filename"].startswith("field-project-photo-13-")), None)
    field = field or next(iter(email_images), featured)
    if main is not None:
        main.clear()
        main.append(soupify(f"""
<div class="w-form rr-project-index">
  <div class="filter-reset-padding">
    <div class="w-clearfix"><div><h6>Example Projects</h6></div></div>
  </div>
  <h1>Example Projects</h1>
  <p>Real project photos and videos from Extreme Buildouts LLC field work, including mechanical rooms, overhead utilities, equipment areas, ductwork, and rough-in coordination.</p>
  <div class="rr-project-index-grid">
    <a class="rr-project-index-card project-card w-inline-block" href="{DETAIL_ROUTE}">
      <img class="image-29" src="{featured['src']}" alt="{DETAIL_TITLE}"/>
      <div class="filter-cards"><h6 class="project-name">{DETAIL_TITLE}</h6><h5 class="project-card-location">Mechanical room piping, A/C coordination, plumbing, equipment, controls, and field buildout photos.</h5></div>
    </a>
    <a class="rr-project-index-card project-card w-inline-block" href="{DETAIL_ROUTE}#field-gallery">
      <img class="image-29" src="{field['src']}" alt="Additional field project examples"/>
      <div class="filter-cards"><h6 class="project-name">Additional Field Project Examples</h6><h5 class="project-card-location">Ductwork, overhead utilities, equipment staging, rooftop work, rough-in, and active commercial buildout conditions.</h5></div>
    </a>
  </div>
</div>
"""))
    add_projects_nav(base)
    write_soup(PUBLIC / "projects.html", base)


def add_home_teaser(media):
    path = PUBLIC / "home.html"
    soup = read_soup(path)
    if soup.find(class_="rr-project-teaser"):
        return
    ensure_project_css(soup)
    featured = [m for m in media if m["type"] == "chat-image"]
    section = soupify(f"""
<section class="padding white-block w-clearfix rr-project-teaser">
  <div class="homepage-content-left float-right">
    <img alt="{DETAIL_TITLE}" class="full-width-image home-page-services" src="{featured[0]['src']}"/>
  </div>
  <div class="homepage-content-right">
    <h5 class="h5 rr-project-eyebrow">Example Project</h5>
    <h2 class="heading-110">{DETAIL_TITLE}</h2>
    <p class="paragraph">Real jobsite photos from a commercial mechanical room buildout showing A/C, plumbing, electrical, equipment, controls, overhead pipe runs, and field coordination before closeout.</p>
    <a class="button underlined-text w-button" href="{DETAIL_ROUTE}">View Project Photos</a>
  </div>
</section>
""")
    footer = soup.find("footer")
    if footer is not None:
        footer.insert_before(section)
    elif soup.body is not None:
        soup.body.append(section)
    add_projects_nav(soup)
    write_soup(path, soup)


def update_footer_and_nav_all():
    for path in PUBLIC.rglob("*.html"):
        if path.name.endswith(".ref"):
            continue
        soup = read_soup(path)
        add_projects_nav(soup)
        write_soup(path, soup)


def update_sitemap():
    path = PUBLIC / "sitemap.xml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    additions = [
        f"  <url><loc>{DOMAIN}{INDEX_ROUTE}</loc></url>",
        f"  <url><loc>{DOMAIN}{DETAIL_ROUTE}</loc></url>",
    ]
    for line in additions:
        if line not in text:
            text = text.replace("</urlset>", f"{line}\n</urlset>")
    path.write_text(text, encoding="utf-8")


def update_llms():
    path = PUBLIC / "llms.txt"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    block = f"\n## Example Projects\n- {DOMAIN}{INDEX_ROUTE}\n- {DOMAIN}{DETAIL_ROUTE}\n"
    if "## Example Projects" not in text:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def main():
    media = json.loads(MEDIA_JSON.read_text(encoding="utf-8"))
    build_project_detail(media)
    build_projects_index(media)
    add_home_teaser(media)
    update_footer_and_nav_all()
    update_sitemap()
    update_llms()
    print("add-project-gallery: projects page, detail page, nav, sitemap, and homepage teaser updated")


if __name__ == "__main__":
    main()
