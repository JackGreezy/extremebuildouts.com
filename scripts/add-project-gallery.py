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
.rr-project-index{max-width:1180px;margin:0 auto}
.rr-project-index h1,.rr-project-page h1{max-width:980px}
.rr-project-index>p,.rr-project-lede{max-width:880px!important;color:#455666!important}
.rr-project-index-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:34px 0 22px}
.rr-project-index-card{display:flex!important;min-height:100%;flex-direction:column;background:#fff!important;border:1px solid rgba(69,85,102,.18)!important;text-decoration:none!important;color:inherit!important;box-shadow:0 10px 28px rgba(20,34,48,.07)!important;overflow:hidden}
.rr-project-index-card img{display:block!important;width:100%!important;aspect-ratio:4/3!important;height:auto!important;object-fit:cover!important;transition:transform .22s ease}
.rr-project-index-card:hover img{transform:scale(1.035)}
.rr-project-card-copy{display:flex!important;min-height:160px!important;flex-direction:column!important;justify-content:space-between!important;padding:22px!important}
.rr-project-card-title{margin:0!important;color:#101820!important;font-size:20px!important;line-height:1.12!important;letter-spacing:0!important;text-transform:none!important}
.rr-project-card-text{margin:12px 0 0!important;font-size:15px!important;line-height:1.42!important;color:#455666!important;letter-spacing:0!important;text-transform:none!important}
.rr-project-index-strip{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin:22px 0 0}
.rr-project-index-strip img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover}
.rr-project-page{max-width:1220px;margin:0 auto}
.rr-project-hero-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(360px,.95fr);gap:34px;align-items:end;margin-bottom:34px}
.rr-project-hero-media{background:#101820;border:1px solid rgba(69,85,102,.18);box-shadow:0 16px 34px rgba(20,34,48,.12)}
.rr-project-hero-media img{display:block;width:100%;aspect-ratio:5/4;object-fit:cover}
.rr-project-section{margin:44px 0}
.rr-project-section-heading{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:18px}
.rr-project-section-heading h2{margin-bottom:0!important}
.rr-project-section-heading p{max-width:540px!important;margin:0!important;color:#455666!important}
.rr-project-gallery{display:grid;grid-auto-flow:dense;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px;margin:18px 0 0}
.rr-project-gallery figure{position:relative;grid-column:span 4;margin:0;background:#101820;border:1px solid rgba(69,85,102,.18);box-shadow:0 8px 22px rgba(20,34,48,.06);overflow:hidden}
.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6){grid-column:span 6}
.rr-project-gallery img{display:block;width:100%;aspect-ratio:4/3;height:auto;object-fit:cover}
.rr-project-gallery figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;background:linear-gradient(180deg,rgba(16,24,32,0),rgba(16,24,32,.82));font-weight:800;color:#fff;line-height:1.24;text-shadow:0 1px 12px rgba(0,0,0,.35)}
.rr-project-gallery.rr-field-gallery figure{grid-column:span 3}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6){grid-column:span 6}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:span 4}
.rr-project-gallery.rr-field-gallery img{aspect-ratio:1/1}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1) img,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6) img{aspect-ratio:16/9}
.rr-project-video{margin:18px 0 0;background:#111;border:1px solid rgba(69,85,102,.22);box-shadow:0 14px 32px rgba(20,34,48,.12)}
.rr-project-video video{display:block;width:100%;max-height:680px;background:#111}
.rr-project-metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:26px 0 10px}
.rr-project-metrics div{border:1px solid rgba(69,85,102,.18);padding:18px 20px;background:#fff}
.rr-project-metrics strong{display:block;color:#009b67;font-size:24px;line-height:1}
.rr-project-metrics span{display:block;margin-top:6px;font-weight:700;color:#455666}
.rr-taxonomy-intro{max-width:1120px;margin:10px 0 32px}
.rr-taxonomy-intro h1{margin:18px 0 14px!important}
.rr-taxonomy-intro p{max-width:980px!important;color:#455666!important}
.rr-taxonomy-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:22px}
.rr-taxonomy-card-grid div{border:1px solid rgba(69,85,102,.18);background:#fff;padding:18px 20px;box-shadow:0 8px 22px rgba(20,34,48,.05)}
.rr-taxonomy-card-grid strong{display:block;color:#009b67;text-transform:uppercase;letter-spacing:.08em;font-size:13px;margin-bottom:8px}
.rr-taxonomy-card-grid span{display:block;color:#455666;font-weight:700;line-height:1.35}
.rr-site-footer{background:#101820!important;color:#fff!important;padding:0!important}
.rr-site-footer a{color:#dfe9ef!important;text-decoration:none!important}
.rr-site-footer a:hover{color:#fff!important;text-decoration:underline!important;text-decoration-thickness:1px!important;text-underline-offset:4px!important}
.rr-footer-inner{max-width:1220px;margin:0 auto;padding:54px 30px 34px}
.rr-footer-top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px;align-items:end;padding-bottom:34px;border-bottom:1px solid rgba(255,255,255,.14)}
.rr-footer-brand .rr-wordmark{display:inline-flex!important;flex-direction:column!important;gap:0!important;margin-bottom:18px!important}
.rr-footer-brand p{max-width:720px!important;margin:0!important;color:#c8d3db!important;font-size:17px!important;line-height:1.55!important}
.rr-footer-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.rr-footer-button{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:46px!important;padding:12px 18px!important;border:1px solid rgba(255,255,255,.28)!important;background:#009b67!important;color:#fff!important;font-weight:800!important;line-height:1!important}
.rr-footer-button-alt{background:transparent!important;color:#fff!important}
.rr-footer-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:24px;margin-top:34px}
.rr-footer-col h2{margin:0 0 13px!important;color:#fff!important;font-size:15px!important;line-height:1.2!important;letter-spacing:.08em!important;text-transform:uppercase!important}
.rr-footer-col a{display:block!important;margin:0 0 8px!important;color:#dfe9ef!important;font-size:14px!important;line-height:1.28!important}
.rr-footer-bottom{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:34px;padding-top:22px;border-top:1px solid rgba(255,255,255,.14);color:#aebbc4;font-size:13px}
@media(max-width:1100px){.rr-project-index-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.rr-project-gallery figure,.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6),.rr-project-gallery.rr-field-gallery figure,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:span 6}.rr-project-hero-grid{grid-template-columns:1fr}}
@media(max-width:1100px){.rr-footer-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.rr-footer-top{grid-template-columns:1fr}.rr-footer-actions{justify-content:flex-start}}
@media(max-width:800px){.rr-project-index-grid,.rr-project-index-strip,.rr-project-metrics{grid-template-columns:1fr}.rr-project-gallery{grid-template-columns:1fr}.rr-project-gallery figure,.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6),.rr-project-gallery.rr-field-gallery figure,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:auto}.rr-project-section-heading{display:block}.rr-project-video video{max-height:none}.rr-footer-grid{grid-template-columns:1fr 1fr}.rr-footer-inner{padding:42px 20px 28px}}
@media(max-width:800px){.rr-taxonomy-card-grid{grid-template-columns:1fr}}
@media(max-width:520px){.rr-footer-grid{grid-template-columns:1fr}.rr-footer-actions{display:grid;grid-template-columns:1fr}.rr-footer-button{width:100%}}
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


FOOTER_COLUMNS = [
    (
        "Services",
        [
            ("Retail Buildouts", "/services/retail-buildouts"),
            ("Tenant Improvements", "/services/tenant-improvement-buildouts"),
            ("Design-Build", "/services/design-build-construction"),
            ("Commercial A/C", "/services/commercial-ac-buildouts"),
            ("Electrical", "/services/electrical-buildout-services"),
            ("Plumbing", "/services/plumbing-buildout-services"),
            ("Ground-Up", "/services/ground-up-construction"),
            ("All Services", "/services"),
        ],
    ),
    (
        "Project Types",
        [
            ("Retail Stores", "/building-types/retail-stores-shopping-centers"),
            ("Restaurants", "/building-types/restaurants-food-service-spaces"),
            ("Office Suites", "/building-types/office-professional-suites"),
            ("Medical Offices", "/building-types/medical-office-clinics"),
            ("Warehouses", "/building-types/warehouses-light-industrial"),
            ("Ground-Up Shells", "/building-types/shell-buildings-ground-up"),
            ("Custom Homes", "/building-types/custom-homes-residential-renovations"),
            ("All Project Types", "/building-types"),
        ],
    ),
    (
        "Industries",
        [
            ("Property Owners", "/industries/property-owners-developers"),
            ("Franchise Retail", "/industries/franchise-retail-operators"),
            ("Restaurants", "/industries/restaurant-hospitality-operators"),
            ("Facility Managers", "/industries/facility-managers"),
            ("Commercial Landlords", "/industries/commercial-landlords"),
            ("Homeowners", "/industries/homeowners-investors"),
            ("All Industries", "/industries"),
        ],
    ),
    (
        "Houston Area",
        [
            ("Houston", "/locations/houston-tx"),
            ("Spring", "/locations/spring-tx"),
            ("The Woodlands", "/locations/the-woodlands-tx"),
            ("Conroe", "/locations/conroe-tx"),
            ("Tomball", "/locations/tomball-tx"),
            ("Cypress", "/locations/cypress-tx"),
            ("Katy", "/locations/katy-tx"),
            ("Sugar Land", "/locations/sugar-land-tx"),
            ("Pearland", "/locations/pearland-tx"),
            ("League City", "/locations/league-city-tx"),
        ],
    ),
    (
        "DFW Area",
        [
            ("DFW Area", "/locations/dfw-area"),
            ("Dallas", "/locations/dallas-tx"),
            ("Fort Worth", "/locations/fort-worth-tx"),
            ("Arlington", "/locations/arlington-tx"),
            ("Plano", "/locations/plano-tx"),
            ("Frisco", "/locations/frisco-tx"),
            ("McKinney", "/locations/mckinney-tx"),
            ("Irving", "/locations/irving-tx"),
            ("Grand Prairie", "/locations/grand-prairie-tx"),
            ("Denton", "/locations/denton-tx"),
        ],
    ),
    (
        "Company",
        [
            ("East Texas", "/locations/east-texas"),
            ("Tyler", "/locations/tyler-tx"),
            ("Longview", "/locations/longview-tx"),
            ("Projects", "/projects"),
            ("About", "/about"),
            ("Contact", "/contact"),
            ("Privacy", "/privacy"),
            ("Terms", "/terms"),
        ],
    ),
]


def build_footer_markup():
    columns = []
    for heading, links in FOOTER_COLUMNS:
        items = "".join(
            f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'
            for label, href in links
        )
        columns.append(f'<div class="rr-footer-col"><h2>{html.escape(heading)}</h2>{items}</div>')
    return f"""
<footer class="primary-footer refresh-footer rr-site-footer">
  <div class="rr-footer-inner">
    <div class="rr-footer-top">
      <div class="rr-footer-brand">
        <a class="rr-wordmark" href="/"><span class="rr-wm-1">Extreme</span><span class="rr-wm-2">Buildouts LLC</span></a>
        <p>Commercial and residential buildouts, A/C, electrical, plumbing, design-build, retail finish-outs, renovations, and ground-up construction across East Texas, Greater Houston, and Dallas-Fort Worth.</p>
      </div>
      <div class="rr-footer-actions">
        <a class="rr-footer-button" href="/contact">Request a Buildout Review</a>
        <a class="rr-footer-button rr-footer-button-alt" href="mailto:hello@extremebuildouts.com">hello@extremebuildouts.com</a>
      </div>
    </div>
    <div class="rr-footer-grid">{''.join(columns)}</div>
    <div class="rr-footer-bottom">
      <span>Extreme Buildouts LLC</span>
      <span>Commercial and residential construction. A/C, electrical, and plumbing coordinated in house.</span>
    </div>
  </div>
</footer>
"""


def replace_footer(soup):
    footer = soup.find("footer")
    rich_footer = soupify(build_footer_markup())
    if footer is not None:
        footer.replace_with(rich_footer)
    elif soup.body is not None:
        soup.body.append(rich_footer)


def gallery(items, captions, extra_class="", gallery_id=None):
    attrs = f' class="rr-project-gallery {extra_class}"'
    if gallery_id:
        attrs += f' id="{html.escape(gallery_id, quote=True)}"'
    out = [f"<div{attrs}>"]
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
            '<section class="rr-project-section" id="walkthrough-video">'
            '<div class="rr-project-section-heading"><h2>Field Walkthrough</h2>'
            '<p>Active buildout conditions, overhead coordination, equipment access, and rough-in sequencing from the jobsite.</p></div>'
            f'<div class="rr-project-video"><video controls muted playsinline preload="metadata" poster="{html.escape(poster, quote=True)}">'
            f'<source src="{html.escape(video["src"], quote=True)}" type="video/mp4"/>'
            "</video></div></section>"
        )
    return (
        '<div class="rr-project-hero-grid"><div><h6>Example Project</h6><h1>Commercial Mechanical Room Buildout</h1>'
        '<p class="rr-project-lede">Real jobsite photos from a commercial mechanical room buildout with A/C, plumbing, electrical, controls, overhead pipe runs, equipment areas, and field coordination tied into one working scope.</p>'
        '<div class="rr-project-metrics"><div><strong>MEP</strong><span>A/C, plumbing, electrical, and controls</span></div><div><strong>Field</strong><span>Real project photos from active work</span></div><div><strong>Scope</strong><span>Mechanical room and utility coordination</span></div></div>'
        '</div><div class="rr-project-hero-media">'
        f'<img src="{html.escape(featured[0]["src"], quote=True)}" alt="{html.escape(DETAIL_TITLE, quote=True)}"/>'
        '</div></div>'
        '<section class="rr-project-section" id="primary-gallery"><div class="rr-project-section-heading"><h2>Primary Mechanical Photos</h2>'
        '<p>Controls, valves, metering, insulated pipe runs, service clearances, equipment staging, and utility routing from the same project.</p></div>'
        + gallery(featured, featured_captions)
        + '</section>'
        + video_html
        + '<section class="rr-project-section" id="field-gallery"><div class="rr-project-section-heading"><h2>Additional Field Examples</h2>'
        '<p>Ductwork, ceiling utilities, structural openings, rooftop equipment, rough-in work, lifts, equipment staging, and active commercial buildout conditions.</p></div>'
        + gallery(field, field_captions, "rr-field-gallery")
        + '</section><section class="rr-project-section"><h2>What This Shows Owners</h2>'
        '<p>Commercial buildouts are not just finish work. The finished space depends on what happens in mechanical rooms, above ceilings, behind walls, on rooftops, and around equipment clearances. Extreme Buildouts LLC uses that field reality to plan scopes before the project turns into disconnected trade visits.</p>'
        '<p>If a space needs A/C, electrical, plumbing, structural coordination, interior finish work, or ground-up planning, this is the kind of detail that should be reviewed early. The goal is a space that opens cleanly, works correctly, and does not leave the owner chasing unresolved trade gaps after construction.</p>'
        '<h2>Ready to plan the scope?</h2><a class="button underlined-text w-button" href="/contact">Request a Buildout Review</a></section>'
    )


def build_project_detail(media):
    base = read_soup(PUBLIC / "services/commercial-ac-buildouts.html")
    ensure_project_css(base)
    set_meta(base, DETAIL_TITLE, DESCRIPTION, DETAIL_ROUTE)
    old = base.select_one("section.padding")
    section = soupify(
        f'<section class="padding rr-project-page"><div class="rr-project-detail">{project_body(media)}</div></section>'
    )
    if old is not None:
        old.replace_with(section)
    elif base.body is not None:
        base.body.insert(1, section)
    add_projects_nav(base)
    write_soup(PUBLIC / "projects/mechanical-room-buildout.html", base)


def build_projects_index(media):
    base = read_soup(PUBLIC / "services.html")
    ensure_project_css(base)
    set_meta(base, INDEX_TITLE, "Example project photos and videos from Extreme Buildouts LLC.", INDEX_ROUTE)
    main = base.select_one("body > .padding")
    featured_images = [m for m in media if m["type"] == "chat-image"]
    featured = featured_images[0]
    email_images = [m for m in media if m["type"] == "email-image"]
    video = next((m for m in media if m["type"] == "video"), None)
    field = next((m for m in email_images if m["filename"].startswith("field-project-photo-22-")), None)
    field = field or next((m for m in email_images if m["filename"].startswith("field-project-photo-13-")), None)
    field = field or next(iter(email_images), featured)
    strip_items = featured_images[:3] + email_images[:3]
    strip = "".join(
        f'<img loading="lazy" src="{html.escape(item["src"], quote=True)}" alt="{html.escape(item["label"], quote=True)}"/>'
        for item in strip_items
    )
    video_poster = (video or {}).get("poster", featured["src"])
    if main is not None:
        main.clear()
        main.append(soupify(f"""
<div class="rr-project-index">
  <div class="filter-reset-padding">
    <div class="w-clearfix"><div><h6>Example Projects</h6></div></div>
  </div>
  <h1>Example Projects</h1>
  <p>Real project photos and videos from Extreme Buildouts LLC field work, including mechanical rooms, overhead utilities, equipment areas, ductwork, and rough-in coordination.</p>
  <div class="rr-project-index-grid">
    <a class="rr-project-index-card w-inline-block" href="{DETAIL_ROUTE}">
      <img class="image-29" src="{featured['src']}" alt="{DETAIL_TITLE}"/>
      <div class="rr-project-card-copy"><h2 class="rr-project-card-title">{DETAIL_TITLE}</h2><p class="rr-project-card-text">Mechanical room piping, A/C coordination, plumbing, equipment, controls, and field buildout photos.</p></div>
    </a>
    <a class="rr-project-index-card w-inline-block" href="{DETAIL_ROUTE}#primary-gallery">
      <img class="image-29" src="{featured_images[2]['src']}" alt="Primary mechanical photos"/>
      <div class="rr-project-card-copy"><h2 class="rr-project-card-title">Primary Mechanical Photos</h2><p class="rr-project-card-text">Controls, pipe routing, equipment access, metering, valves, and service clearances from active work.</p></div>
    </a>
    <a class="rr-project-index-card w-inline-block" href="{DETAIL_ROUTE}#walkthrough-video">
      <img class="image-29" src="{video_poster}" alt="Field walkthrough video"/>
      <div class="rr-project-card-copy"><h2 class="rr-project-card-title">Field Walkthrough</h2><p class="rr-project-card-text">Active buildout conditions, overhead coordination, equipment access, and rough-in sequencing from the jobsite.</p></div>
    </a>
    <a class="rr-project-index-card w-inline-block" href="{DETAIL_ROUTE}#field-gallery">
      <img class="image-29" src="{field['src']}" alt="Additional field project examples"/>
      <div class="rr-project-card-copy"><h2 class="rr-project-card-title">Additional Field Project Examples</h2><p class="rr-project-card-text">Ductwork, overhead utilities, equipment staging, rooftop work, rough-in, and active commercial buildout conditions.</p></div>
    </a>
  </div>
  <div class="rr-project-index-strip">{strip}</div>
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
        ensure_project_css(soup)
        replace_footer(soup)
        write_soup(path, soup)


INDEX_COPY = {
    "services.html": {
        "eyebrow": "Services",
        "title": "Buildout Services",
        "body": (
            "Extreme Buildouts LLC handles commercial and residential construction work with A/C, "
            "electrical, plumbing, renovation, tenant improvement, and ground-up planning tied into one field scope. "
            "Each service starts with existing conditions, owner goals, trade conflicts, inspection needs, and the schedule pressure behind the work."
        ),
        "cards": [
            ("Planning", "Site walks, utility review, layout decisions, and budget alternates before crews mobilize."),
            ("Trades", "A/C, electrical, plumbing, framing, finishes, equipment, and punch work sequenced together."),
            ("Turnover", "A usable finished space with clear closeout, service access, and fewer unresolved trade gaps."),
        ],
    },
    "building-types.html": {
        "eyebrow": "Project Types",
        "title": "Construction By Building Type",
        "body": (
            "Retail suites, restaurants, offices, medical spaces, warehouses, homes, and shell buildings all need different construction decisions. "
            "Extreme Buildouts LLC reviews the way the property will be used, how people move through it, and which trade systems have to support the finished layout."
        ),
        "cards": [
            ("Commercial", "Tenant improvements, restaurants, offices, medical suites, retail spaces, and light industrial work."),
            ("Residential", "Remodels, additions, comfort upgrades, utility changes, and finish work inside occupied homes."),
            ("Ground Up", "Site access, shell work, MEP rough-in, interior buildout, inspections, and final turnover."),
        ],
    },
    "industries.html": {
        "eyebrow": "Industries",
        "title": "Construction For Owners And Operators",
        "body": (
            "Property owners, franchise operators, restaurants, landlords, facility managers, homeowners, and investors need scopes that match real operating pressure. "
            "Extreme Buildouts LLC plans around downtime, tenant coordination, equipment requirements, finish expectations, and the work that has to be complete before occupancy."
        ),
        "cards": [
            ("Operators", "Opening dates, brand standards, customer areas, equipment, and finish details kept in sequence."),
            ("Owners", "Budget clarity, field verification, lease obligations, and long-term maintenance considered early."),
            ("Facilities", "Repairs, renovations, trade upgrades, and phased work planned around active properties."),
        ],
    },
    "locations.html": {
        "eyebrow": "Service Areas",
        "title": "Texas Buildout Service Areas",
        "body": (
            "Extreme Buildouts LLC serves East Texas, Greater Houston, and the DFW area with practical buildout planning and field execution. "
            "The work changes by market: urban tenant improvements, suburban retail, restaurants, medical suites, homes, warehouses, and ground-up projects all bring different access, utility, and scheduling constraints."
        ),
        "cards": [
            ("East Texas", "Retail, residential, light commercial, and renovation work across Tyler, Longview, Marshall, Texarkana, and Nacogdoches."),
            ("Houston Area", "Commercial buildouts, restaurants, medical spaces, homes, and utility-heavy scopes across greater Houston."),
            ("DFW Area", "Tenant improvements, offices, retail, restaurants, warehouses, and residential work across Dallas-Fort Worth suburbs."),
        ],
    },
}


def enhance_taxonomy_indexes():
    for filename, copy_block in INDEX_COPY.items():
        path = PUBLIC / filename
        if not path.exists():
            continue
        soup = read_soup(path)
        if soup.find(class_="rr-taxonomy-intro"):
            continue
        ensure_project_css(soup)
        target = soup.select_one(".filter-reset-padding")
        if target is None:
            continue
        cards = "".join(
            f"<div><strong>{html.escape(label)}</strong><span>{html.escape(text)}</span></div>"
            for label, text in copy_block["cards"]
        )
        intro = soupify(
            f"""
<section class="rr-taxonomy-intro">
  <h6>{html.escape(copy_block["eyebrow"])}</h6>
  <h1>{html.escape(copy_block["title"])}</h1>
  <p>{html.escape(copy_block["body"])}</p>
  <div class="rr-taxonomy-card-grid">{cards}</div>
</section>
"""
        )
        target.insert_after(intro)
        write_soup(path, soup)


def clean_not_found_copy():
    path = PUBLIC / "404.html"
    if not path.exists():
        return
    soup = read_soup(path)
    changed = False
    for node in soup.find_all(string=True):
        text = str(node)
        updated = text.replace("Page not found", "Not Found")
        updated = updated.replace(
            "The page you are looking for is not available. Return to the main site or contact Extreme Buildouts LLC to discuss your project.",
            "That route is not available. Return to the main site or contact Extreme Buildouts LLC to discuss your project.",
        )
        if updated != text:
            node.replace_with(NavigableString(updated))
            changed = True
    if changed:
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


def strip_generated_html_whitespace():
    for path in PUBLIC.rglob("*.html"):
        if path.name.endswith(".ref"):
            continue
        text = path.read_text(encoding="utf-8")
        lines = []
        for line in text.splitlines():
            while " \t" in line:
                line = line.replace(" \t", "\t")
            lines.append(line.rstrip())
        cleaned = "\n".join(lines) + "\n"
        if cleaned != text:
            path.write_text(cleaned, encoding="utf-8")


def main():
    media = json.loads(MEDIA_JSON.read_text(encoding="utf-8"))
    build_project_detail(media)
    build_projects_index(media)
    add_home_teaser(media)
    enhance_taxonomy_indexes()
    clean_not_found_copy()
    update_footer_and_nav_all()
    update_sitemap()
    update_llms()
    strip_generated_html_whitespace()
    print("add-project-gallery: projects page, detail page, nav, sitemap, and homepage teaser updated")


if __name__ == "__main__":
    main()
