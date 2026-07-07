const sgMail = require("@sendgrid/mail");

const rateStore = new Map();
const RATE_LIMIT = 5;
const RATE_WINDOW_MS = 15 * 60 * 1000;
const TEMPLATE_ID =
  process.env.SENDGRID_TEMPLATE_ID || "d-15217ab1c55347b5847c2421b1a82847";

function checkRateLimit(ip) {
  const now = Date.now();
  const entry = rateStore.get(ip);
  if (!entry || now > entry.resetTime) {
    rateStore.set(ip, { count: 1, resetTime: now + RATE_WINDOW_MS });
    return { limited: false, remaining: RATE_LIMIT - 1, resetTime: now + RATE_WINDOW_MS };
  }
  if (entry.count >= RATE_LIMIT) {
    return { limited: true, remaining: 0, resetTime: entry.resetTime };
  }
  entry.count += 1;
  return {
    limited: false,
    remaining: Math.max(0, RATE_LIMIT - entry.count),
    resetTime: entry.resetTime,
  };
}

function parseBody(req) {
  if (req.body && typeof req.body === "object") return req.body;
  if (typeof req.body === "string") {
    const type = req.headers["content-type"] || "";
    if (type.includes("application/json")) return JSON.parse(req.body || "{}");
    return Object.fromEntries(new URLSearchParams(req.body));
  }
  return {};
}

function readField(body, ...keys) {
  for (const key of keys) {
    const value = body[key];
    if (value !== undefined && value !== null && String(value).trim()) {
      return String(value).trim();
    }
  }
  return "";
}

function normalizePhone(value) {
  return String(value || "").replace(/\D/g, "");
}

async function verifyTurnstile(token, remoteip) {
  const secret = process.env.TURNSTILE_SECRET || process.env.TURNSTILE_SECRET_KEY;
  if (!process.env.NEXT_PUBLIC_TURNSTILE_SITE_KEY) return true;
  if (!secret || !token) return false;

  const body = new URLSearchParams({ secret, response: token });
  if (remoteip) body.set("remoteip", remoteip);

  const response = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body,
  });
  const data = await response.json().catch(() => ({}));
  return data.success === true;
}

function getBrand(submittedDate) {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://extremebuildouts.com";
  const businessEmail =
    process.env.BUSINESS_EMAIL ||
    process.env.SENDGRID_FROM_EMAIL ||
    "hello@extremebuildouts.com";

  return {
    subject: "We received your buildout review request",
    preheader:
      "Thanks for your inquiry. Extreme Buildouts LLC received your project details.",
    company_name: "Extreme Buildouts LLC",
    logo_url: `${siteUrl.replace(/\/$/, "")}/logo.png`,
    city_state: "Texas",
    brand_accent: "#c6c8ca",
    cta_dark_bg: "#050505",
    bg_color: "#f3f3f1",
    text_dark: "#141516",
    text_muted: "#4d5358",
    text_body: "#202326",
    text_faint: "#747a80",
    border_color: "#c6c8ca",
    card_header_bg: "#f7f7f7",
    hero_title: "Thanks for your inquiry. We received your buildout review request.",
    hero_subtitle:
      "The team will review your details and follow up about scope, schedule, and next steps.",
    details_title: "Project details",
    call_cta_label: "Call Now",
    call_phone: process.env.BUSINESS_PHONE || "",
    call_phone_plain: normalizePhone(process.env.BUSINESS_PHONE),
    site_cta_label: "Go To Site",
    site_url: siteUrl,
    address_line: process.env.BUSINESS_ADDRESS || "Texas",
    footer_note: "This confirmation is a transactional email related to your request.",
    submitted_date: submittedDate,
    brand_title: "Extreme Buildouts LLC",
    brand_tagline:
      "Commercial and residential construction with A/C, electrical, and plumbing coordinated in house.",
    brand_dark_bg: "#050505",
    brand_gold: "#c6c8ca",
    supportPhone: process.env.BUSINESS_PHONE || "",
    supportEmail: businessEmail,
    service_area: "East Texas, Greater Houston, and Dallas-Fort Worth",
    portfolio_url: `${siteUrl.replace(/\/$/, "")}/projects`,
    portfolio_blurb:
      "Retail buildouts, commercial A/C, electrical, plumbing, design-build, renovations, and ground-up construction.",
    intro_copy:
      "Extreme Buildouts LLC reviews buildout scope, utilities, schedule, and field conditions as one coordinated construction plan.",
  };
}

async function sendTemplateEmail(to, from, brand, lead) {
  await sgMail.send({
    to,
    from,
    templateId: TEMPLATE_ID,
    dynamicTemplateData: { ...brand, lead },
  });
}

async function sendEmails(brand, lead) {
  if (!process.env.SENDGRID_API_KEY) {
    console.warn("SENDGRID_API_KEY not set, skipping SendGrid emails");
    return;
  }

  sgMail.setApiKey(process.env.SENDGRID_API_KEY);

  const fromEmail =
    process.env.SENDGRID_FROM_EMAIL ||
    process.env.BUSINESS_EMAIL ||
    "hello@extremebuildouts.com";
  const from = { email: fromEmail, name: process.env.SENDGRID_FROM_NAME || brand.company_name };

  const recipients = [
    process.env.CONTRACTOR_EMAIL,
    process.env.RANKHOUND_NOTIFICATION_EMAIL || "rankhoundseo@gmail.com",
    ...(process.env.CONTACT_NOTIFICATION_RECIPIENTS || "")
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean),
  ].filter(Boolean);

  const sends = [];
  if (lead.email) sends.push(sendTemplateEmail(lead.email, from, brand, lead));
  for (const recipient of [...new Set(recipients)]) {
    sends.push(sendTemplateEmail(recipient, from, brand, lead));
  }
  await Promise.all(sends);
}

async function sendZapier(payload) {
  const webhook = (process.env.ZAPIER_WEBHOOK || "").trim();
  if (!webhook) return;
  const url = webhook.endsWith("/") ? webhook : `${webhook}/`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (!response.ok) {
      console.error("Zapier webhook failed", response.status, await response.text().catch(() => ""));
    }
  } catch (error) {
    console.error("Zapier webhook error", error);
  } finally {
    clearTimeout(timeout);
  }
}

module.exports = async function handler(req, res) {
  const clientIp =
    String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() ||
    req.headers["x-real-ip"] ||
    "unknown";
  const rate = checkRateLimit(clientIp);
  res.setHeader("X-RateLimit-Limit", String(RATE_LIMIT));
  res.setHeader("X-RateLimit-Remaining", String(rate.remaining));
  res.setHeader("X-RateLimit-Reset", String(rate.resetTime));

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }
  if (rate.limited) {
    const retryAfter = Math.ceil((rate.resetTime - Date.now()) / 1000);
    res.setHeader("Retry-After", String(retryAfter));
    return res.status(429).json({ error: "Rate limit exceeded. Please try again later." });
  }

  try {
    const body = parseBody(req);
    if (body.honeypot) return res.status(200).json({ success: true });

    const token = body["cf-turnstile-response"];
    if (!(await verifyTurnstile(token, clientIp))) {
      return res.status(400).json({ error: "Captcha verification failed" });
    }

    const lead = {
      name: readField(body, "name", "fullName"),
      email: readField(body, "email", "emailAddress"),
      phone: normalizePhone(readField(body, "phone", "phoneNumber")),
      phone_plain: normalizePhone(readField(body, "phone", "phoneNumber")),
      projectType: readField(body, "projectType", "serviceType", "service") || "Buildout Review",
      projectDescription: readField(body, "details", "projectDetails", "message"),
      timeline: readField(body, "timeline"),
      address: readField(body, "projectAddress", "company", "address"),
      city: readField(body, "city") || "Texas",
    };

    if (!lead.name || !lead.email || !lead.phone) {
      return res.status(400).json({ error: "Name, phone, and email are required." });
    }

    const submittedDate = new Date().toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    const brand = getBrand(submittedDate);
    const payload = {
      ...body,
      lead,
      contractorEmail: process.env.CONTRACTOR_EMAIL || "",
      projectType: lead.projectType,
      source: process.env.NEXT_PUBLIC_SOURCE || "Extreme Buildouts LLC Website",
      website_url: process.env.NEXT_PUBLIC_SITE_URL || "https://extremebuildouts.com",
      timestamp: new Date().toISOString(),
      submitted_at: new Date().toISOString(),
      _meta: { site: "extreme-buildouts", route: "/api/submit" },
    };

    await sendZapier(payload);
    await sendEmails(brand, lead);
    return res.status(200).json({ success: true });
  } catch (error) {
    console.error("Error processing form submission", error);
    return res.status(500).json({ error: "Internal server error" });
  }
};
