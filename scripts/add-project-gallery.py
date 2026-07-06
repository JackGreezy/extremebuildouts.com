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
LOGO_SRC = "/logo.png"
FAVICON_SRC = "/favicon.png"
APPLE_ICON_SRC = "/apple-touch-icon.png"

DETAIL_ROUTE = "/projects/mechanical-room-buildout"
INDEX_ROUTE = "/projects"
DETAIL_TITLE = "Commercial Mechanical Room Buildout"
INDEX_TITLE = "Example Projects"
DESCRIPTION = (
    "Example project photos from Extreme Buildouts LLC showing commercial mechanical room, "
    "A/C piping, plumbing, equipment, ductwork, and field buildout coordination."
)
ABOUT_DESCRIPTION = (
    "Extreme Buildouts LLC coordinates commercial and residential construction, retail buildouts, "
    "A/C, electrical, plumbing, design-build, renovations, and ground-up work across Texas."
)
CONTACT_DESCRIPTION = (
    "Send Extreme Buildouts LLC the project address, space type, schedule, known utility needs, "
    "and construction work you want reviewed."
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
:root{--eb-black:#050505;--eb-graphite:#141516;--eb-charcoal:#202326;--eb-gunmetal:#3f4448;--eb-steel:#747a80;--eb-silver:#c6c8ca;--eb-bright:#f7f7f7}
html body{background:#f3f3f1!important;color:#141516!important}
.rr-project-teaser{background:#f7f7f7}
.rr-project-eyebrow{color:#5f6469!important;text-transform:uppercase!important;letter-spacing:.12em!important;font-weight:800!important}
.rr-project-index{max-width:1180px;margin:0 auto}
.rr-project-index h1,.rr-project-page h1{max-width:980px}
.rr-project-index>p,.rr-project-lede{max-width:880px!important;color:#4d5358!important}
.rr-project-index-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:34px 0 22px}
.rr-project-index-card{display:flex!important;min-height:100%;flex-direction:column;background:#fff!important;border:1px solid rgba(20,21,22,.16)!important;text-decoration:none!important;color:inherit!important;box-shadow:0 10px 28px rgba(5,5,5,.08)!important;overflow:hidden}
.rr-project-index-card img{display:block!important;width:100%!important;aspect-ratio:4/3!important;height:auto!important;object-fit:cover!important;transition:transform .22s ease}
.rr-project-index-card:hover img{transform:scale(1.035)}
.rr-project-card-copy{display:flex!important;min-height:160px!important;flex-direction:column!important;justify-content:space-between!important;padding:22px!important}
.rr-project-card-title{margin:0!important;color:#101112!important;font-size:20px!important;line-height:1.12!important;letter-spacing:0!important;text-transform:none!important}
.rr-project-card-text{margin:12px 0 0!important;font-size:15px!important;line-height:1.42!important;color:#4d5358!important;letter-spacing:0!important;text-transform:none!important}
.rr-project-index-strip{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin:22px 0 0}
.rr-project-index-strip img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover}
.rr-project-page{max-width:1220px;margin:0 auto}
.rr-project-hero-grid{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(360px,.95fr);gap:34px;align-items:end;margin-bottom:34px}
.rr-project-hero-media{background:#050505;border:1px solid rgba(198,200,202,.28);box-shadow:0 16px 34px rgba(5,5,5,.18)}
.rr-project-hero-media img{display:block;width:100%;aspect-ratio:5/4;object-fit:cover}
.rr-project-section{margin:44px 0}
.rr-project-section-heading{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-bottom:18px}
.rr-project-section-heading h2{margin-bottom:0!important}
.rr-project-section-heading p{max-width:540px!important;margin:0!important;color:#4d5358!important}
.rr-project-gallery{display:grid;grid-auto-flow:dense;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px;margin:18px 0 0}
.rr-project-gallery figure{position:relative;grid-column:span 4;margin:0;background:#050505;border:1px solid rgba(20,21,22,.18);box-shadow:0 8px 22px rgba(5,5,5,.08);overflow:hidden}
.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6){grid-column:span 6}
.rr-project-gallery img{display:block;width:100%;aspect-ratio:4/3;height:auto;object-fit:cover}
.rr-project-gallery figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 14px 12px;background:linear-gradient(180deg,rgba(5,5,5,0),rgba(5,5,5,.86));font-weight:800;color:#fff;line-height:1.24;text-shadow:0 1px 12px rgba(0,0,0,.35)}
.rr-project-gallery.rr-field-gallery figure{grid-column:span 3}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6){grid-column:span 6}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:span 4}
.rr-project-gallery.rr-field-gallery img{aspect-ratio:1/1}
.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1) img,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6) img{aspect-ratio:16/9}
.rr-project-video{margin:18px 0 0;background:#050505;border:1px solid rgba(198,200,202,.24);box-shadow:0 14px 32px rgba(5,5,5,.16)}
.rr-project-video video{display:block;width:100%;max-height:680px;background:#050505}
.rr-project-metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:26px 0 10px}
.rr-project-metrics div{border:1px solid rgba(20,21,22,.16);padding:18px 20px;background:#fff}
.rr-project-metrics strong{display:block;color:#202326;font-size:24px;line-height:1}
.rr-project-metrics span{display:block;margin-top:6px;font-weight:700;color:#4d5358}
.rr-home-hero{position:relative;min-height:calc(100vh - 76px);background:#050505;color:#fff;overflow:hidden}
.rr-home-hero-track{position:relative;min-height:inherit}
.rr-home-hero-slide{position:absolute;inset:0;opacity:0;pointer-events:none;transition:opacity .55s ease}
.rr-home-hero-slide.is-active{opacity:1;pointer-events:auto}
.rr-home-hero-slide img{position:absolute;inset:0;display:block;width:100%;height:100%;object-fit:cover}
.rr-home-hero-slide:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.56) 32%,rgba(0,0,0,.22) 66%,rgba(0,0,0,.08) 100%)}
.rr-home-hero-copy{position:relative;z-index:2;display:flex;min-height:calc(100vh - 76px);max-width:720px;flex-direction:column;justify-content:center;padding:86px 0 104px 9.5vw}
.rr-home-hero-kicker{margin:0 0 18px;color:#fff;font-size:14px;font-weight:850;letter-spacing:.18em;line-height:1;text-transform:uppercase;text-shadow:0 2px 14px rgba(0,0,0,.8)}
.rr-home-hero-title{margin:0 0 18px;color:#fff;font-size:clamp(36px,4.6vw,72px);font-weight:900;line-height:.96;letter-spacing:0;text-shadow:0 2px 16px rgba(0,0,0,.82)}
.rr-home-hero-text{max-width:660px;margin:0;color:#fff;font-size:clamp(16px,1.25vw,21px);font-weight:750;line-height:1.48;text-shadow:0 2px 14px rgba(0,0,0,.86)}
.rr-home-hero-cta{margin-top:26px}
.rr-home-hero-arrow{position:absolute;z-index:5;top:50%;display:flex;width:54px;height:54px;align-items:center;justify-content:center;margin:0;padding:0;background:rgba(5,5,5,.44);border:1px solid rgba(247,247,247,.64);border-radius:0;color:#fff;font-size:34px;line-height:1;transform:translateY(-50%);box-shadow:0 12px 28px rgba(0,0,0,.24);cursor:pointer}
.rr-home-hero-arrow:hover,.rr-home-hero-arrow:focus{background:#f7f7f7;color:#050505;border-color:#f7f7f7;outline:none}
.rr-home-hero-prev{left:28px}
.rr-home-hero-next{right:28px}
.rr-home-hero-dots{position:absolute;z-index:6;left:9.5vw;bottom:36px;display:flex;gap:9px}
.rr-home-hero-dot{width:34px;height:3px;margin:0;padding:0;background:rgba(247,247,247,.42);border:0;border-radius:0;cursor:pointer}
.rr-home-hero-dot.is-active{background:#f7f7f7}
.rr-taxonomy-intro{max-width:1120px;margin:10px 0 32px}
.rr-taxonomy-intro h1{margin:18px 0 14px!important}
.rr-taxonomy-intro p{max-width:980px!important;color:#4d5358!important}
.rr-taxonomy-card-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:22px}
.rr-taxonomy-card-grid div{border:1px solid rgba(20,21,22,.16);background:#fff;padding:18px 20px;box-shadow:0 8px 22px rgba(5,5,5,.06)}
.rr-taxonomy-card-grid strong{display:block;color:#202326;text-transform:uppercase;letter-spacing:.08em;font-size:13px;margin-bottom:8px}
.rr-taxonomy-card-grid span{display:block;color:#4d5358;font-weight:700;line-height:1.35}
.rr-site-footer{background:linear-gradient(180deg,#111213,#050505)!important;color:#fff!important;padding:0!important;border-top:1px solid rgba(198,200,202,.22)!important}
.rr-site-footer a{color:#d8dadc!important;text-decoration:none!important}
.rr-site-footer a:hover{color:#fff!important;text-decoration:underline!important;text-decoration-thickness:1px!important;text-underline-offset:4px!important}
.rr-logo-link{display:inline-flex!important;align-items:center!important;justify-content:flex-start!important;text-decoration:none!important;line-height:0!important;flex:0 0 auto!important}
.rr-site-logo{display:block!important;width:100%!important;height:auto!important;max-width:100%!important;object-fit:contain!important}
.navigation-top-simple{background:linear-gradient(180deg,#0d0d0e,#1a1c1e)!important;border-bottom:1px solid rgba(198,200,202,.2)!important;box-shadow:0 8px 26px rgba(0,0,0,.2)!important}
.navigation-top-simple .navbar-container{background:transparent!important}
.navigation-top-simple .rr-logo-link{width:clamp(158px,15vw,220px)!important;min-width:158px!important;height:66px!important;align-items:center!important}
.navigation-top-simple .rr-site-logo{width:auto!important;max-width:100%!important;max-height:60px!important}
.navigation-top-simple .refresh-navlinks.top{color:#f1f1f1!important;text-shadow:none!important}
.navigation-top-simple .refresh-navlinks.top:hover{color:#c6c8ca!important}
.navigation-top-simple .rr-burger{color:#f7f7f7!important}
.navigation-top-simple .rr-burger span{background:#f7f7f7!important}
.featured-content-box.white h6,.featured-content-box.white h3,.featured-content-box.white .paragraph.white,.featured-content-box.white .news-hero{color:#fff!important;opacity:1!important;text-shadow:0 2px 14px rgba(0,0,0,.82)!important}
.featured-content-box.white .news-hero{max-width:650px!important;font-weight:750!important;line-height:1.48!important}
.overlay.gradient-left-right{background:linear-gradient(90deg,rgba(0,0,0,.76) 0%,rgba(0,0,0,.52) 34%,rgba(0,0,0,.18) 68%,rgba(0,0,0,.06) 100%)!important;opacity:1!important}
.hero-button{display:inline-flex!important;align-items:center!important;min-height:0!important;padding:0!important;margin-top:22px!important;background:transparent!important;border:0!important;box-shadow:none!important}
.button,.w-button,.hero-button div{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:46px!important;width:auto!important;max-width:100%!important;margin:0!important;padding:13px 22px!important;background:linear-gradient(180deg,#2a2c2f 0%,#070707 100%)!important;color:#f7f7f7!important;border:1px solid rgba(198,200,202,.78)!important;border-radius:2px!important;text-shadow:none!important;box-shadow:0 12px 26px rgba(5,5,5,.18)!important;font-size:12px!important;font-weight:900!important;line-height:1.05!important;letter-spacing:.06em!important;text-transform:uppercase!important;text-decoration:none!important;white-space:normal!important;overflow-wrap:anywhere!important}
.button:hover,.w-button:hover,.hero-button div:hover{background:linear-gradient(180deg,#f7f7f7 0%,#b8bdc1 100%)!important;color:#050505!important;border-color:#050505!important;box-shadow:0 14px 30px rgba(5,5,5,.22)!important}
.button.underlined-text:before,.button.underlined-text:after,.w-button.underlined-text:before,.w-button.underlined-text:after{display:none!important;content:none!important}
.rr-burger{margin-left:auto!important}
html body [data-rr-mobile]{right:0!important;margin-right:0!important;width:min(86vw,320px)!important;max-width:min(86vw,320px)!important;transform:translateX(125%)!important;transition:transform .25s!important}
html body.rr-nav-open [data-rr-mobile]{transform:translateX(0)!important;width:min(86vw,320px)!important;max-width:min(86vw,320px)!important}
.rr-footer-inner{max-width:1220px;margin:0 auto;padding:54px 30px 34px}
.rr-footer-top{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:30px;align-items:end;padding-bottom:34px;border-bottom:1px solid rgba(198,200,202,.18)}
.rr-footer-brand .rr-footer-logo-link{width:min(340px,100%)!important;margin-bottom:18px!important}
.rr-footer-brand .rr-site-logo{max-height:96px!important}
.rr-footer-brand p{max-width:720px!important;margin:0!important;color:#d8dadc!important;font-size:17px!important;line-height:1.55!important}
.rr-footer-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end}
.rr-footer-button{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:46px!important;padding:13px 22px!important;border:1px solid rgba(198,200,202,.74)!important;border-radius:2px!important;background:linear-gradient(180deg,#2a2c2f,#070707)!important;color:#f7f7f7!important;font-size:12px!important;font-weight:900!important;line-height:1.05!important;letter-spacing:.06em!important;text-transform:uppercase!important;text-decoration:none!important}
.rr-footer-button:hover{background:linear-gradient(180deg,#f7f7f7,#b8bdc1)!important;color:#050505!important;border-color:#050505!important}
.rr-footer-button-alt{background:transparent!important;color:#f7f7f7!important;border-color:rgba(198,200,202,.46)!important}
.rr-footer-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:24px;margin-top:34px}
.rr-footer-col h2{margin:0 0 13px!important;color:#fff!important;font-size:15px!important;line-height:1.2!important;letter-spacing:.08em!important;text-transform:uppercase!important}
.rr-footer-col a{display:block!important;margin:0 0 8px!important;color:#d8dadc!important;font-size:14px!important;line-height:1.28!important}
.rr-footer-bottom{display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-top:34px;padding-top:22px;border-top:1px solid rgba(198,200,202,.18);color:#b8bdc1;font-size:13px}
@media(max-width:1100px){.rr-project-index-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.rr-project-gallery figure,.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6),.rr-project-gallery.rr-field-gallery figure,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:span 6}.rr-project-hero-grid{grid-template-columns:1fr}}
@media(max-width:1100px){.rr-footer-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.rr-footer-top{grid-template-columns:1fr}.rr-footer-actions{justify-content:flex-start}}
@media(max-width:800px){.navigation-top-simple .navbar-container{position:relative!important;padding-right:8px!important}.navigation-top-simple .rr-logo-link{width:min(48vw,190px)!important;min-width:145px!important;height:58px!important}.navigation-top-simple .rr-site-logo{max-height:52px!important}.navigation-top-simple .rr-burger{position:absolute!important;right:6px!important;top:50%!important;transform:translateY(-50%)!important;margin:0!important;padding:8px 0 8px 8px!important}.rr-home-hero,.rr-home-hero-track,.rr-home-hero-copy{min-height:560px}.rr-home-hero-copy{padding:92px 26px 136px}.rr-home-hero-arrow{top:auto;bottom:76px;width:38px;height:38px;font-size:26px;transform:none;background:rgba(5,5,5,.64);box-shadow:0 10px 22px rgba(0,0,0,.28)}.rr-home-hero-prev{left:auto;right:74px}.rr-home-hero-next{right:26px}.rr-home-hero-dots{left:26px;bottom:30px}.rr-project-index-grid,.rr-project-index-strip,.rr-project-metrics{grid-template-columns:1fr}.rr-project-gallery{grid-template-columns:1fr}.rr-project-gallery figure,.rr-project-gallery figure:nth-child(1),.rr-project-gallery figure:nth-child(8n+6),.rr-project-gallery.rr-field-gallery figure,.rr-project-gallery.rr-field-gallery figure:nth-child(10n+1),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+6),.rr-project-gallery.rr-field-gallery figure:nth-child(10n+4){grid-column:auto}.rr-project-section-heading{display:block}.rr-project-video video{max-height:none}.rr-footer-grid{grid-template-columns:1fr 1fr}.rr-footer-inner{padding:42px 20px 28px}}
@media(max-width:800px){.rr-taxonomy-card-grid{grid-template-columns:1fr}}
@media(max-width:520px){.rr-footer-grid{grid-template-columns:1fr}.rr-footer-actions{display:grid;grid-template-columns:1fr}.rr-footer-button{width:100%}}
</style>
"""


def ensure_project_css(soup):
    if soup.head and not soup.find(id="rr-project-gallery-css"):
        soup.head.append(soupify(PROJECT_CSS))


def set_icon_links(soup):
    if soup.head is None:
        return
    for tag in list(soup.find_all("link")):
        rel = tag.get("rel", [])
        if isinstance(rel, str):
            rel_text = rel.lower()
        else:
            rel_text = " ".join(rel).lower()
        if "icon" in rel_text:
            tag.decompose()
    for rel, href, type_value in (
        ("icon", FAVICON_SRC, "image/png"),
        ("shortcut icon", FAVICON_SRC, "image/png"),
        ("apple-touch-icon", APPLE_ICON_SRC, None),
    ):
        tag = soup.new_tag("link")
        tag["rel"] = rel
        tag["href"] = href
        if type_value:
            tag["type"] = type_value
        soup.head.append(tag)


def logo_anchor(soup, anchor, footer=False):
    classes = [c for c in anchor.get("class", []) if c != "rr-wordmark"]
    for cls in ("rr-logo-link", "rr-footer-logo-link" if footer else "rr-header-logo-link"):
        if cls not in classes:
            classes.append(cls)
    anchor["class"] = classes
    anchor["href"] = anchor.get("href") or "/"
    anchor["aria-label"] = BIZ
    anchor.clear()
    img = soup.new_tag("img", src=LOGO_SRC, alt=BIZ)
    img["class"] = ["rr-site-logo"]
    anchor.append(img)


def replace_text_logos(soup):
    for anchor in soup.select("a.rr-wordmark"):
        logo_anchor(soup, anchor, footer=anchor.find_parent("footer") is not None)
    for anchor in soup.select("header a.refresh-logo, header a.w-nav-brand"):
        if anchor.find("img", src=LOGO_SRC):
            continue
        logo_anchor(soup, anchor, footer=False)


def neutralize_old_wordmark_css(soup):
    replacements = {
        "rr-wordmark": "rr-old-text-logo",
        "rr-wm-1": "rr-old-text-logo-1",
        "rr-wm-2": "rr-old-text-logo-2",
    }
    for style in soup.find_all("style"):
        if not style.string:
            continue
        text = str(style.string)
        updated = text
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            style.string.replace_with(updated)


FINAL_BRAND_CSS = """
<style id="rr-final-brand-css">
header.navigation-top-simple{background:linear-gradient(180deg,#080809,#181a1c)!important;border-bottom:1px solid rgba(198,200,202,.26)!important;box-shadow:0 10px 28px rgba(0,0,0,.24)!important;min-height:76px!important}
header.navigation-top-simple .navbar-container{background:transparent!important;min-height:76px!important;padding:0 54px!important;display:flex!important;align-items:center!important}
header.navigation-top-simple a.rr-logo-link.refresh-logo{width:clamp(158px,14vw,220px)!important;min-width:158px!important;max-width:220px!important;height:68px!important;padding:0!important;margin:0!important;display:flex!important;align-items:center!important;overflow:visible!important}
header.navigation-top-simple .rr-site-logo{display:block!important;width:auto!important;height:auto!important;max-width:100%!important;max-height:62px!important;object-fit:contain!important}
header.navigation-top-simple .nav-menu-2,header.navigation-top-simple .nav-menu-2>.w-dropdown{background:transparent!important}
header.navigation-top-simple .refresh-navlinks.top{color:#f5f5f5!important;font-weight:800!important;text-shadow:none!important}
header.navigation-top-simple .refresh-navlinks.top:hover{color:#c6c8ca!important}
header.navigation-top-simple .rr-burger{color:#f5f5f5!important;background:transparent!important}
header.navigation-top-simple .rr-burger span{background:#f5f5f5!important}
body .heading-110,body .homepage-content-right h2,body .rr-project-card-title,body .rr-taxonomy-intro h1,body .rr-taxonomy-intro h2{color:#141516!important}
body .h5,body .h6-reeduced,body .rr-project-eyebrow,body .homepage-content-right h6:not(.white){color:#5f6469!important}
body .paragraph,body .rr-project-card-text,body .rr-project-lede,body .rr-taxonomy-intro p{color:#4d5358!important}
body .featured-content-box.white h6,body .featured-content-box.white h3,body .featured-content-box.white .paragraph.white,body .featured-content-box.white .news-hero{color:#fff!important;opacity:1!important;text-shadow:0 2px 14px rgba(0,0,0,.82)!important}
body .featured-content-box.white .news-hero{max-width:650px!important;font-weight:750!important;line-height:1.48!important}
body .overlay.gradient-left-right{background:linear-gradient(90deg,rgba(0,0,0,.76) 0%,rgba(0,0,0,.52) 34%,rgba(0,0,0,.18) 68%,rgba(0,0,0,.06) 100%)!important;opacity:1!important}
body .hero-button{display:inline-flex!important;align-items:center!important;min-height:0!important;padding:0!important;margin-top:22px!important;background:transparent!important;border:0!important;box-shadow:none!important}
body .button,body .w-button,body .hero-button div{display:inline-flex!important;align-items:center!important;justify-content:center!important;min-height:46px!important;width:auto!important;max-width:100%!important;margin:0!important;padding:13px 22px!important;background:linear-gradient(180deg,#2a2c2f 0%,#070707 100%)!important;color:#f7f7f7!important;border:1px solid rgba(198,200,202,.78)!important;border-radius:2px!important;text-shadow:none!important;box-shadow:0 12px 26px rgba(5,5,5,.18)!important;font-size:12px!important;font-weight:900!important;line-height:1.05!important;letter-spacing:.06em!important;text-transform:uppercase!important;text-decoration:none!important;white-space:normal!important;overflow-wrap:anywhere!important}
body .button:hover,body .w-button:hover,body .hero-button div:hover{background:linear-gradient(180deg,#f7f7f7 0%,#b8bdc1 100%)!important;color:#050505!important;border-color:#050505!important;box-shadow:0 14px 30px rgba(5,5,5,.22)!important}
body .button.underlined-text:before,body .button.underlined-text:after,body .w-button.underlined-text:before,body .w-button.underlined-text:after{display:none!important;content:none!important}
body .hero-button{display:inline-flex!important;align-items:center!important;min-height:0!important;padding:0!important;background:transparent!important;border:0!important;box-shadow:none!important}
footer.rr-site-footer{background:linear-gradient(180deg,#111213,#050505)!important;border-top:1px solid rgba(198,200,202,.26)!important}
footer.rr-site-footer .rr-footer-logo-link{display:inline-flex!important;width:min(340px,100%)!important;max-width:340px!important;margin-bottom:18px!important}
footer.rr-site-footer .rr-site-logo{width:100%!important;height:auto!important;max-height:none!important}
footer.rr-site-footer .rr-footer-button{background:linear-gradient(180deg,#2a2c2f,#070707)!important;color:#f7f7f7!important;border:1px solid rgba(198,200,202,.74)!important;border-radius:2px!important}
footer.rr-site-footer .rr-footer-button:hover{background:linear-gradient(180deg,#f7f7f7,#b8bdc1)!important;color:#050505!important;border-color:#050505!important}
footer.rr-site-footer .rr-footer-button-alt{color:#f7f7f7!important;background:transparent!important;border-color:rgba(198,200,202,.46)!important}
footer.rr-site-footer .rr-footer-button-alt:hover{background:#f7f7f7!important;color:#050505!important;border-color:#050505!important}
@media(max-width:980px){
  header.navigation-top-simple{min-height:68px!important}
  header.navigation-top-simple .navbar-container{position:relative!important;min-height:68px!important;padding:0 8px 0 18px!important}
  header.navigation-top-simple a.rr-logo-link.refresh-logo{width:min(48vw,190px)!important;min-width:145px!important;max-width:190px!important;height:60px!important}
  header.navigation-top-simple .rr-site-logo{max-height:54px!important}
  header.navigation-top-simple .rr-burger{position:absolute!important;right:6px!important;top:50%!important;transform:translateY(-50%)!important;margin:0!important;padding:8px 0 8px 8px!important}
}
@media(max-width:420px){
  header.navigation-top-simple .navbar-container{padding:0 6px 0 14px!important}
  header.navigation-top-simple a.rr-logo-link.refresh-logo{width:min(46vw,168px)!important;min-width:132px!important;height:56px!important}
  header.navigation-top-simple .rr-site-logo{max-height:50px!important}
  header.navigation-top-simple .rr-burger{right:4px!important}
}
</style>
"""


def ensure_final_brand_css(soup):
    if soup.head is None:
        return
    for style in soup.find_all("style", id="rr-final-brand-css"):
        style.decompose()
    soup.head.append(soupify(FINAL_BRAND_CSS))


def set_brand_assets(soup):
    set_icon_links(soup)
    replace_text_logos(soup)
    neutralize_old_wordmark_css(soup)
    ensure_final_brand_css(soup)


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
        <a class="rr-logo-link rr-footer-logo-link" href="/" aria-label="{html.escape(BIZ, quote=True)}"><img class="rr-site-logo" src="{LOGO_SRC}" alt="{html.escape(BIZ, quote=True)}"/></a>
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


def pick_media(media, filename, fallback):
    return next((m for m in media if m.get("filename") == filename), fallback)


def build_home_hero_markup(media):
    fallback = next((m for m in media if m["type"] == "chat-image"), media[0])
    slide_specs = [
        (
            pick_media(media, "example-mechanical-room-01-mechanical-piping-controls.jpg", fallback),
            "Commercial Mechanical Room Buildout",
            "A/C, plumbing, electrical, controls, and mechanical piping coordinated inside one working project scope.",
        ),
        (
            pick_media(media, "example-mechanical-room-02-mechanical-room-pipe-runs.jpg", fallback),
            "Pipe Runs, Equipment, And Access",
            "Mechanical room pathways, service clearances, and equipment access planned before the finished space turns over.",
        ),
        (
            pick_media(media, "example-mechanical-room-03-overhead-mechanical-piping.jpg", fallback),
            "Overhead Utility Coordination",
            "Piping, supports, ceiling conflicts, and trade sequencing reviewed before closeout work locks the space in.",
        ),
        (
            pick_media(media, "example-mechanical-room-04-mechanical-infrastructure-wide.jpg", fallback),
            "Buildouts With Field Reality",
            "A/C, plumbing, electrical, ductwork, controls, and finish work coordinated from active jobsite conditions.",
        ),
        (
            pick_media(media, "field-project-photo-03-20240923-200528.jpg", fallback),
            "Commercial Interior Systems",
            "Ductwork, overhead utilities, and open-ceiling coordination tied into retail and commercial buildout planning.",
        ),
    ]
    slides = []
    dots = []
    for index, (item, title, text) in enumerate(slide_specs):
        active = " is-active" if index == 0 else ""
        hidden = "false" if index == 0 else "true"
        src = html.escape(item["src"], quote=True)
        alt = html.escape(title, quote=True)
        slides.append(
            f"""
<article class="rr-home-hero-slide{active}" data-rr-hero-slide aria-hidden="{hidden}">
  <img src="{src}" alt="{alt}" loading="{'eager' if index == 0 else 'lazy'}"/>
  <div class="rr-home-hero-copy">
    <p class="rr-home-hero-kicker">Example Project</p>
    <h1 class="rr-home-hero-title">{html.escape(title)}</h1>
    <p class="rr-home-hero-text">{html.escape(text)}</p>
    <div class="rr-home-hero-cta"><a class="button underlined-text w-button" href="/contact">Request a Buildout Review</a></div>
  </div>
</article>
"""
        )
        dots.append(
            f'<button class="rr-home-hero-dot{active}" type="button" aria-label="Show project image {index + 1}" data-rr-hero-dot="{index}"></button>'
        )
    return soupify(
        f"""
<section class="rr-home-hero" data-rr-home-hero>
  <div class="rr-home-hero-track">
    {''.join(slides)}
  </div>
  <button class="rr-home-hero-arrow rr-home-hero-prev" type="button" aria-label="Previous project image" data-rr-hero-prev>&#8249;</button>
  <button class="rr-home-hero-arrow rr-home-hero-next" type="button" aria-label="Next project image" data-rr-hero-next>&#8250;</button>
  <div class="rr-home-hero-dots" aria-label="Project image selector">{''.join(dots)}</div>
</section>
<script id="rr-home-hero-script">
(function(){{
  var root=document.querySelector('[data-rr-home-hero]');
  if(!root) return;
  var slides=Array.prototype.slice.call(root.querySelectorAll('[data-rr-hero-slide]'));
  var dots=Array.prototype.slice.call(root.querySelectorAll('[data-rr-hero-dot]'));
  var prev=root.querySelector('[data-rr-hero-prev]');
  var next=root.querySelector('[data-rr-hero-next]');
  var current=0;
  var timer=null;
  function show(index){{
    if(!slides.length) return;
    current=(index+slides.length)%slides.length;
    slides.forEach(function(slide,i){{
      var active=i===current;
      slide.classList.toggle('is-active',active);
      slide.setAttribute('aria-hidden',active?'false':'true');
    }});
    dots.forEach(function(dot,i){{
      var active=i===current;
      dot.classList.toggle('is-active',active);
      dot.setAttribute('aria-current',active?'true':'false');
    }});
  }}
  function move(step){{show(current+step);}}
  function stop(){{if(timer) window.clearInterval(timer); timer=null;}}
  function start(){{stop(); timer=window.setInterval(function(){{move(1);}},6200);}}
  if(prev) prev.addEventListener('click',function(){{move(-1); start();}});
  if(next) next.addEventListener('click',function(){{move(1); start();}});
  dots.forEach(function(dot){{dot.addEventListener('click',function(){{show(Number(dot.getAttribute('data-rr-hero-dot'))||0); start();}});}});
  root.addEventListener('mouseenter',stop);
  root.addEventListener('mouseleave',start);
  document.addEventListener('visibilitychange',function(){{if(document.hidden) stop(); else start();}});
  show(0);
  start();
}})();
</script>
"""
    )


def replace_home_hero(media):
    path = PUBLIC / "home.html"
    soup = read_soup(path)
    existing = soup.find(attrs={"data-rr-home-hero": True})
    if existing is not None:
        existing.decompose()
    old_script = soup.find("script", id="rr-home-hero-script")
    if old_script is not None:
        old_script.decompose()
    hero = build_home_hero_markup(media)
    slider = soup.select_one(".slider.w-slider")
    if slider is not None:
        slider.replace_with(hero)
    else:
        header = soup.find("header")
        if header is not None:
            header.insert_after(hero)
        elif soup.body is not None:
            soup.body.insert(0, hero)
    ensure_project_css(soup)
    add_projects_nav(soup)
    write_soup(path, soup)


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
        set_brand_assets(soup)
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


def expand_about_page():
    path = PUBLIC / "about.html"
    if not path.exists():
        return
    soup = read_soup(path)
    set_meta(soup, "About Extreme Buildouts LLC", ABOUT_DESCRIPTION, "/about")
    ensure_project_css(soup)
    current = soup.select_one("body > .padding")
    grid = current.select_one(".grid-8") if current is not None else None
    if grid is not None:
        grid.clear()
        grid.append(
            soupify(
                """
<h1>About Extreme Buildouts LLC</h1>
<p class="paragraph-emphasized">Extreme Buildouts LLC handles commercial and residential construction with A/C, electrical, plumbing, design-build, renovation, retail finish-out, and ground-up work coordinated under one roof.</p>
<p class="paragraph">The company is built for owners who need the field work, trade sequencing, utility planning, finishes, and closeout handled as one practical construction scope. Every project starts with the intended use of the space, existing conditions, access, schedule, inspections, equipment needs, and the owner decisions that affect price or timing.</p>
"""
            )
        )
    if soup.find(class_="rr-about-depth"):
        write_soup(path, soup)
        return
    body = soup.body
    section = soupify(
        """
<section class="padding rr-about-depth">
  <div class="rr-taxonomy-intro">
    <h6>How We Work</h6>
    <h2>Construction, A/C, electrical, and plumbing under one plan</h2>
    <p>Extreme Buildouts LLC is built for owners who need one accountable construction team to look at the full job, not a stack of disconnected trade visits. A retail buildout, restaurant finish-out, office renovation, home addition, warehouse upgrade, or ground-up project can all depend on the same field reality: walls, ceilings, utilities, equipment, inspections, access, schedule, and cleanup have to line up before the space is ready.</p>
    <p>The work starts with existing conditions and the intended use of the property. Crews look at service access, rough-in paths, fixture and equipment locations, ceiling conflicts, shutdown windows, finish expectations, and the owner decisions that affect price or schedule. That review gives the project a cleaner order before demolition, framing, A/C, electrical, plumbing, finishes, and punch work begin.</p>
    <div class="rr-taxonomy-card-grid">
      <div><strong>In-House Coordination</strong><span>A/C, electrical, plumbing, construction sequencing, finish work, and closeout are planned together.</span></div>
      <div><strong>Commercial And Residential</strong><span>Retail, restaurants, offices, warehouses, homes, renovations, additions, and ground-up work are handled with practical field planning.</span></div>
      <div><strong>Owner Clarity</strong><span>Scopes identify what is included, what needs field verification, and which decisions should be made before crews mobilize.</span></div>
    </div>
  </div>
</section>
"""
    )
    if current is not None:
        current.insert_after(section)
    elif body is not None:
        body.append(section)
    write_soup(path, soup)


def clean_contact_page():
    path = PUBLIC / "contact.html"
    if not path.exists():
        return
    soup = read_soup(path)
    set_meta(soup, "Start a buildout review", CONTACT_DESCRIPTION, "/contact")
    ensure_project_css(soup)
    rich = soup.select_one(".section-grid .paragraph.w-richtext")
    if rich is not None:
        rich.clear()
        rich.append(
            soupify(
                """
<p>Send the project address or area, space type, schedule, known utility needs, and the work you want priced. Extreme Buildouts LLC will review the construction scope and return practical next steps.</p>
"""
            )
        )
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
    replace_home_hero(media)
    add_home_teaser(media)
    enhance_taxonomy_indexes()
    expand_about_page()
    clean_contact_page()
    clean_not_found_copy()
    update_footer_and_nav_all()
    update_sitemap()
    update_llms()
    strip_generated_html_whitespace()
    print("add-project-gallery: projects page, detail page, homepage hero, nav, sitemap, and homepage teaser updated")


if __name__ == "__main__":
    main()
