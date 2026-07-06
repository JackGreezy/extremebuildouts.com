import fs from 'fs';
import path from 'path';

const project = path.resolve('/Users/jackgreenberg/Desktop/rank-and-rent/David/clones/extremebuildouts.com');
const bizName = 'Extreme Buildouts LLC';
const region = 'Texas';
const turfRoot = path.resolve('/Users/jackgreenberg/Desktop/rank-and-rent/brandon/turf');

const taxTitles = {
  services: 'Services',
  'building-types': 'Project Types',
  industries: 'Industries',
  locations: 'Service Areas',
};

const serviceItems = [
  {
    slug: 'retail-buildouts',
    name: 'Retail Buildouts',
    angle: 'retail suites, shopping center spaces, and storefronts that need to open cleanly',
    use: 'sales floor layout, back-of-house flow, restroom placement, electrical demand, lighting, HVAC zoning, plumbing fixtures, finishes, signage coordination, and the punch list that has to be complete before opening day',
    detail: 'Retail work is sensitive because customers, neighboring tenants, landlords, inspectors, and vendors all touch the schedule. Extreme Buildouts LLC plans the buildout around lease obligations, utility tie-ins, material lead times, and final turnover instead of treating the space like a blank shell.',
    faqs: [
      ['Can a retail buildout be handled after lease signing but before opening?', 'Yes. The work should start with a site walk, landlord requirements, existing utility review, and a clear opening schedule. That gives the project enough structure to price demolition, rough-in, finishes, inspections, and turnover without guessing.'],
      ['What makes retail buildouts different from normal remodeling?', 'Retail work usually has stricter timing, landlord rules, public-facing finishes, signage coordination, and occupancy requirements. A missed rough-in or delayed inspection can move an opening date, so the trades have to be sequenced tightly.'],
    ],
  },
  {
    slug: 'commercial-ac-buildouts',
    name: 'Commercial A/C Buildouts',
    angle: 'commercial spaces that need practical cooling, ventilation, equipment placement, and finish coordination',
    use: 'load review, equipment access, duct routing, curb or platform locations, condensate management, thermostat placement, ceiling coordination, and startup timing',
    detail: 'A/C work affects framing, electrical, ceiling heights, access panels, roof penetrations, and the comfort of the finished space. Extreme Buildouts LLC reviews the mechanical scope with the rest of the construction plan so the system is not treated as an afterthought.',
    faqs: [
      ['When should A/C planning happen on a commercial buildout?', 'A/C planning should happen before framing and ceiling work are locked in. Equipment placement, duct paths, condensate drains, and electrical feeds can change the layout if they are discovered too late.'],
      ['Can A/C work be coordinated with electrical and plumbing?', 'Yes. That is the point of a coordinated buildout. Mechanical, electrical, plumbing, framing, and finish work are reviewed together so one trade does not block another trade or create rework.'],
    ],
  },
  {
    slug: 'electrical-buildout-services',
    name: 'Electrical Buildout Services',
    angle: 'commercial and residential spaces where power, lighting, panels, devices, and equipment feeds need to be planned with the construction scope',
    use: 'panel review, service needs, lighting layout, dedicated circuits, equipment feeds, data pathway coordination, exterior power, controls, and finish device placement',
    detail: 'Electrical work is one of the first scopes that can break a schedule if it is not coordinated early. Extreme Buildouts LLC plans electrical work around the way the space will operate, the equipment it will support, and the inspections needed before walls and ceilings close.',
    faqs: [
      ['What should be checked before electrical rough-in?', 'Panel capacity, dedicated equipment loads, lighting layout, device locations, low-voltage pathways, exterior circuits, and inspection timing should be checked before rough-in begins.'],
      ['Can electrical work be included in a full buildout scope?', 'Yes. Electrical work can be planned with framing, A/C, plumbing, finishes, and equipment placement so the finished space works without late changes or surface-mounted fixes.'],
    ],
  },
  {
    slug: 'plumbing-buildout-services',
    name: 'Plumbing Buildout Services',
    angle: 'spaces that need supply, waste, vent, fixture, grease, restroom, breakroom, or equipment plumbing coordinated with the rest of the buildout',
    use: 'fixture counts, restroom layout, slab or wall access, water heater placement, floor drains, cleanouts, venting, shutoffs, and finish fixture setting',
    detail: 'Plumbing decisions affect layout, slab cuts, wall locations, inspections, finishes, and long-term service access. Extreme Buildouts LLC treats plumbing as part of the construction plan from the first walk so the owner is not left with expensive late changes.',
    faqs: [
      ['Why does plumbing need to be reviewed early?', 'Plumbing can affect wall layout, slab work, fixture placement, and inspection timing. Early review helps avoid finished walls being opened later to solve drain, vent, or supply problems.'],
      ['Can plumbing be coordinated with restaurant or retail equipment?', 'Yes. Equipment rough-ins, floor drains, hand sinks, restrooms, mop sinks, and water heaters should be coordinated with the equipment layout before work starts.'],
    ],
  },
  {
    slug: 'design-build-construction',
    name: 'Design-Build Construction',
    angle: 'owners who need practical planning, trade input, and construction execution connected from the first site walk',
    use: 'scope definition, layout review, trade feasibility, budget alternates, permitting path, schedule planning, material decisions, and field execution',
    detail: 'Design-build work helps owners avoid a plan that looks good on paper but fails when utilities, equipment, budget, or field conditions are reviewed. Extreme Buildouts LLC uses trade input early so the project can move from concept to construction with fewer surprises.',
    faqs: [
      ['What does design-build mean for a small commercial project?', 'It means layout, trade planning, budget, schedule, and construction are handled together instead of being passed from one disconnected group to another.'],
      ['Is design-build useful for renovations?', 'Yes. Renovations often have hidden conditions and tight budgets. Early trade review helps decide what can stay, what needs to move, and what should be priced as an alternate before demolition starts.'],
    ],
  },
  {
    slug: 'ground-up-construction',
    name: 'Ground-Up Construction',
    angle: 'new buildings that need site work, shell construction, utilities, MEP rough-in, interiors, and final turnover planned as one sequence',
    use: 'site access, utility routing, slab planning, framing, envelope, A/C, electrical, plumbing, inspections, finishes, and owner turnover',
    detail: 'Ground-up work succeeds when the early decisions support the final use of the building. Extreme Buildouts LLC plans the construction sequence around utilities, weather, access, inspections, and the future interior instead of separating shell work from finish-out decisions.',
    faqs: [
      ['What should be clarified before a ground-up project starts?', 'Site access, utility availability, building use, rough budget, schedule expectations, inspection requirements, and finish-level expectations should be clarified before pricing is finalized.'],
      ['Can the same team handle shell and interior work?', 'Yes. Keeping shell construction and interior buildout in one coordinated plan reduces gaps between utility rough-in, equipment needs, finish work, and owner turnover.'],
    ],
  },
  {
    slug: 'commercial-renovations',
    name: 'Commercial Renovations',
    angle: 'occupied and vacant commercial buildings that need layout changes, trade upgrades, finishes, and operational planning',
    use: 'demolition, wall changes, ceiling work, lighting, A/C modifications, plumbing changes, flooring, paint, trim, doors, hardware, and punch work',
    detail: 'Commercial renovation work often has to respect tenants, customers, inventory, business hours, and neighboring spaces. Extreme Buildouts LLC plans renovation work around access, dust, noise, utility interruptions, and the sequence needed to keep the property usable.',
    faqs: [
      ['Can renovation work be phased around an active business?', 'Yes. Phasing can separate noisy work, utility shutdowns, dust control, and finish work so the business has a workable plan instead of a single disruptive construction window.'],
      ['What should a renovation scope include?', 'A renovation scope should identify demolition, repairs, trade upgrades, finish selections, exclusions, access rules, schedule assumptions, and the condition of existing walls, ceilings, floors, and utilities.'],
    ],
  },
  {
    slug: 'tenant-improvement-buildouts',
    name: 'Tenant Improvement Buildouts',
    angle: 'leased suites that need a clean path from shell condition to a working commercial space',
    use: 'landlord requirements, existing utilities, space planning, walls, doors, restrooms, A/C, electrical, plumbing, flooring, paint, ceiling, and closeout',
    detail: 'Tenant improvement work has to balance the tenant schedule, lease terms, landlord rules, and field conditions already present in the suite. Extreme Buildouts LLC helps turn that mix into a buildable scope with fewer handoff gaps.',
    faqs: [
      ['What information helps price a tenant improvement buildout?', 'A current floor plan, landlord work letter, photos, target opening date, required equipment, utility needs, and finish expectations all help produce a tighter buildout price.'],
      ['Can tenant improvements include A/C, electrical, and plumbing?', 'Yes. Tenant improvement scopes often include all three trades, especially when a suite changes use or needs new equipment, restrooms, sinks, lighting, or dedicated circuits.'],
    ],
  },
  {
    slug: 'residential-remodeling-additions',
    name: 'Residential Remodeling and Additions',
    angle: 'homes that need construction, A/C, electrical, plumbing, and finish work planned without leaving gaps between trades',
    use: 'kitchens, bathrooms, additions, garage conversions, utility upgrades, lighting, plumbing fixtures, HVAC changes, flooring, trim, paint, and final punch',
    detail: 'Residential remodeling is personal because the work happens where people live. Extreme Buildouts LLC plans the trade sequence, access, dust control, utility interruptions, and finish details so the project has a path from demolition to completion.',
    faqs: [
      ['Can remodeling include mechanical, electrical, and plumbing changes?', 'Yes. Many remodels require all three, especially kitchens, bathrooms, laundry rooms, additions, and garage conversions. Coordinating them early reduces rework.'],
      ['What makes a residential addition harder than a simple remodel?', 'An addition has to connect structure, roofline, slab or foundation, utilities, heating and cooling, finishes, and exterior drainage to the existing home without creating future service problems.'],
    ],
  },
  {
    slug: 'in-house-mep-coordination',
    name: 'In-House MEP Coordination',
    angle: 'projects where A/C, electrical, and plumbing decisions need to be made with the construction schedule instead of after it',
    use: 'trade sequencing, rough-in conflicts, equipment placement, fixture locations, panel and circuit planning, drain paths, duct routing, inspections, and finish protection',
    detail: 'MEP coordination is where many buildouts either stay on track or start drifting. Extreme Buildouts LLC brings mechanical, electrical, and plumbing planning into the same field conversation as framing, ceilings, finishes, and turnover.',
    faqs: [
      ['Why is MEP coordination important on buildouts?', 'Mechanical, electrical, and plumbing systems share walls, ceilings, chases, equipment areas, and inspection windows. Coordinating them prevents conflicts before the work is covered.'],
      ['Can MEP coordination reduce change orders?', 'It can reduce avoidable change orders by finding conflicts early, but hidden conditions and owner changes can still affect the scope. The value is that decisions are made with better field information.'],
    ],
  },
];

const buildingTypeItems = [
  ['retail-stores-shopping-centers', 'Retail Stores and Shopping Centers', 'landlord rules, customer-facing finishes, public access, signage needs, and a hard opening date'],
  ['restaurants-food-service-spaces', 'Restaurants and Food Service Spaces', 'kitchen rough-ins, ventilation coordination, hand sinks, floor drains, electrical demand, dining finishes, and health-review timing'],
  ['office-professional-suites', 'Office and Professional Suites', 'private offices, conference rooms, lighting, data pathways, restrooms, break areas, and finish standards that need to feel complete on move-in day'],
  ['medical-office-clinics', 'Medical Offices and Clinics', 'patient flow, treatment rooms, handwashing locations, equipment power, privacy needs, durable finishes, and careful closeout'],
  ['warehouses-light-industrial', 'Warehouses and Light Industrial Spaces', 'clear heights, roll-up doors, power demand, office buildouts, break areas, restrooms, lighting, ventilation, and durable work areas'],
  ['custom-homes-residential-renovations', 'Custom Homes and Residential Renovations', 'layout changes, additions, kitchens, bathrooms, comfort upgrades, utility changes, and finish work inside occupied homes'],
  ['multi-family-common-areas', 'Multi-Family Common Areas', 'clubhouses, leasing offices, amenities, laundry areas, corridors, service rooms, and occupied-property scheduling'],
  ['shell-buildings-ground-up', 'Shell Buildings and Ground-Up Projects', 'site access, utility paths, slab decisions, framing, envelope work, MEP rough-in, interior buildout, and final turnover'],
];

const industryItems = [
  ['property-owners-developers', 'Property Owners and Developers', 'owners who need scopes that line up with budgets, lease commitments, inspections, and long-term use of the building'],
  ['franchise-retail-operators', 'Franchise and Retail Operators', 'operators who need brand standards, equipment layouts, public-facing finishes, and opening schedules coordinated in the field'],
  ['restaurant-hospitality-operators', 'Restaurant and Hospitality Operators', 'operators who need kitchens, guest areas, plumbing, ventilation, electrical demand, and finish work handled in the right sequence'],
  ['facility-managers', 'Facility Managers', 'managers who need repairs, renovations, trade work, and small capital projects handled without disrupting daily operations'],
  ['homeowners-investors', 'Homeowners and Residential Investors', 'owners who need remodels, additions, turns, and trade upgrades completed with clean communication and practical scheduling'],
  ['commercial-landlords', 'Commercial Landlords', 'landlords who need tenant spaces prepared, improved, repaired, and turned over with clear scope control'],
];

const locationItems = [
  ['east-texas', 'East Texas', 'humid weather, storm seasons, clay soil movement, long drive times between communities, and a mix of retail, residential, and light commercial properties'],
  ['tyler-tx', 'Tyler, TX', 'medical, retail, restaurant, office, and residential projects that often have active occupants and tight turnover schedules'],
  ['longview-tx', 'Longview, TX', 'industrial support spaces, retail corridors, homes, offices, restaurants, and utility-heavy renovation work'],
  ['marshall-tx', 'Marshall, TX', 'small commercial buildings, residential work, historic properties, retail suites, and practical repair scopes'],
  ['texarkana-tx', 'Texarkana, TX', 'commercial and residential work where scheduling, material runs, and utility coordination need to be planned clearly'],
  ['nacogdoches-tx', 'Nacogdoches, TX', 'college-area rentals, homes, offices, restaurants, and local retail spaces that need buildout work with clean finishes'],
  ['houston-tx', 'Houston, TX', 'dense urban sites, medical and restaurant buildouts, warehouse corridors, high humidity, heavy traffic, and demanding inspection schedules'],
  ['spring-tx', 'Spring, TX', 'retail centers, neighborhood restaurants, office suites, residential additions, wooded lots, and north Houston material logistics'],
  ['the-woodlands-tx', 'The Woodlands, TX', 'master-planned commercial centers, medical offices, professional suites, hospitality spaces, and occupied-property scheduling'],
  ['conroe-tx', 'Conroe, TX', 'fast growth, light industrial properties, lake-area homes, retail pads, long utility runs, and mixed new-build and renovation work'],
  ['tomball-tx', 'Tomball, TX', 'suburban retail, small commercial buildings, rural-edge sites, residential remodels, and schedules affected by access and material runs'],
  ['cypress-tx', 'Cypress, TX', 'high-growth retail corridors, tenant suites, restaurants, clinics, homes, and buildouts where traffic and inspections shape the schedule'],
  ['katy-tx', 'Katy, TX', 'retail shell spaces, restaurants, medical suites, west Houston homes, landlord requirements, and finish schedules tied to opening dates'],
  ['sugar-land-tx', 'Sugar Land, TX', 'professional offices, restaurants, retail spaces, medical suites, HOA-sensitive residential work, and polished finish expectations'],
  ['richmond-tx', 'Richmond, TX', 'Fort Bend growth, retail pads, residential additions, rural-edge access, restaurant work, and projects that need utility planning early'],
  ['missouri-city-tx', 'Missouri City, TX', 'commercial remodels, tenant improvements, medical and office spaces, residential work, and southwest Houston traffic constraints'],
  ['rosenberg-tx', 'Rosenberg, TX', 'retail growth, older commercial spaces, warehouse support areas, residential projects, and schedules shaped by material delivery windows'],
  ['pearland-tx', 'Pearland, TX', 'retail corridors, healthcare spaces, restaurants, residential remodels, coastal humidity, and fast-moving south Houston development'],
  ['league-city-tx', 'League City, TX', 'coastal humidity, medical and office suites, restaurants, homes, equipment clearances, and work near bay-area commercial corridors'],
  ['pasadena-tx', 'Pasadena, TX', 'industrial-adjacent commercial properties, restaurants, retail spaces, warehouses, utility-heavy work, and practical finish requirements'],
  ['baytown-tx', 'Baytown, TX', 'industrial support buildings, retail corridors, homes, restaurants, coastal weather, and projects where equipment access matters'],
  ['humble-tx', 'Humble, TX', 'airport-area commercial work, retail centers, restaurants, residential renovations, and north Houston utility coordination'],
  ['kingwood-tx', 'Kingwood, TX', 'wooded residential properties, neighborhood retail, professional suites, humidity control, drainage awareness, and careful finish protection'],
  ['dfw-area', 'DFW Area', 'multi-city logistics, tenant improvement schedules, fast-growing suburbs, office parks, restaurant corridors, and a wide spread between suppliers and jobsites'],
  ['dallas-tx', 'Dallas, TX', 'urban tenant improvements, restaurant and retail buildouts, office renovations, medical suites, traffic constraints, and tight turnover dates'],
  ['fort-worth-tx', 'Fort Worth, TX', 'industrial support spaces, mixed-use corridors, older commercial buildings, restaurants, homes, and practical renovation sequencing'],
  ['arlington-tx', 'Arlington, TX', 'entertainment district work, retail centers, restaurants, light commercial spaces, homes, and schedules affected by events and traffic'],
  ['plano-tx', 'Plano, TX', 'corporate office suites, medical buildouts, restaurants, retail centers, finish-sensitive interiors, and landlord-driven tenant work'],
  ['frisco-tx', 'Frisco, TX', 'new retail pads, restaurant spaces, medical and office suites, high-growth residential work, and tight inspection and opening schedules'],
  ['mckinney-tx', 'McKinney, TX', 'historic commercial buildings, new suburban retail, homes, offices, and renovation scopes that need existing-condition review'],
  ['irving-tx', 'Irving, TX', 'airport and Las Colinas commercial spaces, offices, restaurants, warehouses, and work where access windows can drive the sequence'],
  ['garland-tx', 'Garland, TX', 'light industrial properties, retail suites, restaurants, homes, and utility-heavy remodels that need early trade coordination'],
  ['carrollton-tx', 'Carrollton, TX', 'industrial flex spaces, office suites, restaurants, retail centers, and projects where tenant turnover needs clear phasing'],
  ['richardson-tx', 'Richardson, TX', 'telecom and office corridors, restaurants, medical suites, retail centers, and finish work tied to operational continuity'],
  ['lewisville-tx', 'Lewisville, TX', 'lake-area commercial corridors, retail suites, restaurants, warehouses, homes, and projects between Dallas and Denton suppliers'],
  ['grapevine-tx', 'Grapevine, TX', 'hospitality, retail, restaurant, airport-adjacent commercial work, and finish-sensitive spaces with public-facing deadlines'],
  ['southlake-tx', 'Southlake, TX', 'premium retail, medical offices, residential remodeling, professional suites, and finish standards that need close scope control'],
  ['euless-tx', 'Euless, TX', 'mid-cities retail, office, restaurant, and warehouse spaces where Dallas and Fort Worth logistics meet'],
  ['grand-prairie-tx', 'Grand Prairie, TX', 'warehouse corridors, retail and restaurant work, homes, event-area traffic, and utility coordination between Dallas and Fort Worth'],
  ['north-richland-hills-tx', 'North Richland Hills, TX', 'mid-cities commercial renovations, retail centers, homes, medical suites, and work that needs practical phasing'],
  ['denton-tx', 'Denton, TX', 'college-area retail, restaurants, rentals, offices, homes, and renovation schedules affected by growth north of DFW'],
  ['flower-mound-tx', 'Flower Mound, TX', 'professional suites, residential remodels, retail spaces, restaurants, lake-area logistics, and high finish expectations'],
  ['allen-tx', 'Allen, TX', 'north DFW retail corridors, office suites, restaurants, medical spaces, residential projects, and quick-turn finish schedules'],
];

const locationImageSources = {
  'houston-tx.jpg': 'hometurfhouston.com/public/images/locations/houston-tx.jpg',
  'spring-tx.jpg': 'hometurfhouston.com/public/images/locations/spring-tx.jpg',
  'the-woodlands-tx.jpg': 'artificialgrassofhouston.com/public/images/locations/the-woodlands-tx.jpg',
  'conroe-tx.jpg': 'artificialgrassofhouston.com/public/images/locations/conroe-tx.jpg',
  'tomball-tx.jpg': 'hometurfhouston.com/public/images/locations/tomball-tx.jpg',
  'cypress-tx.jpg': 'hometurfhouston.com/public/images/locations/cypress-tx.jpg',
  'katy-tx.jpg': 'hometurfhouston.com/public/images/locations/katy-tx.jpg',
  'sugar-land-tx.jpg': 'hometurfhouston.com/public/images/locations/sugar-land-tx.jpg',
  'richmond-tx.jpg': 'hometurfhouston.com/public/images/locations/richmond-tx.jpg',
  'missouri-city-tx.jpg': 'hometurfhouston.com/public/images/locations/missouri-city-tx.jpg',
  'rosenberg-tx.jpg': 'hometurfhouston.com/public/images/locations/rosenberg-tx.jpg',
  'pearland-tx.jpg': 'hometurfhouston.com/public/images/locations/pearland-tx.jpg',
  'league-city-tx.jpg': 'hometurfhouston.com/public/images/locations/league-city-tx.jpg',
  'pasadena-tx.jpg': 'hometurfhouston.com/public/images/locations/pasadena-tx.jpg',
  'baytown-tx.jpg': 'hometurfhouston.com/public/images/locations/baytown-tx.jpg',
  'humble-tx.jpg': 'hometurfhouston.com/public/images/locations/humble-tx.jpg',
  'kingwood-tx.jpg': 'artificialgrasskingwood.com/public/images/locations/kingwood-tx.jpg',
  'dfw-area.jpg': 'hometurfdallas.com/public/images/locations/dallas-tx-artificial-turf-installation.jpg',
  'dallas-tx.jpg': 'hometurfdallas.com/public/images/locations/dallas-tx-artificial-turf-installation.jpg',
  'fort-worth-tx.png': 'hometurffortworth.com/public/images/locations/fort-worth-tx-commercial-artificial-turf-installation.png',
  'arlington-tx.jpg': 'hometurfdallas.com/public/images/locations/arlington-tx-artificial-turf-installation.jpg',
  'plano-tx.jpg': 'hometurfdallas.com/public/images/locations/plano-tx-artificial-turf-installation.jpeg',
  'frisco-tx.jpg': 'hometurfdallas.com/public/images/locations/frisco-tx-artificial-turf-installation.jpg',
  'mckinney-tx.jpg': 'hometurfdallas.com/public/images/locations/mckinney-tx-artificial-turf-installation.jpg',
  'irving-tx.jpg': 'hometurfdallas.com/public/images/locations/irving-tx-artificial-turf-installation.jpg',
  'garland-tx.jpg': 'hometurfdallas.com/public/images/locations/garland-tx-artificial-turf-installation.jpg',
  'carrollton-tx.jpg': 'hometurfdallas.com/public/images/locations/carrollton-tx-artificial-turf-installation.jpg',
  'richardson-tx.jpg': 'hometurfdallas.com/public/images/locations/richardson-tx-artificial-turf-installation.jpg',
  'lewisville-tx.jpg': 'hometurfdallas.com/public/images/locations/lewisville-tx-artificial-turf-installation.jpg',
  'grapevine-tx.jpg': 'artificialturfgrapevine.com/public/images/locations/grapevine-tx-artificial-grass-installation.jpg',
  'southlake-tx.jpg': 'artificialturfgrapevine.com/public/images/locations/southlake-tx-artificial-grass-installation.jpg',
  'euless-tx.jpg': 'hometurffortworth.com/public/images/locations/euless-tx-commercial-artificial-turf-installation.jpg',
  'grand-prairie-tx.webp': 'artificialgrassgrandprairie.com/public/images/locations/grand-prairie-tx-commercial-artificial-grass-installation.webp',
  'north-richland-hills-tx.jpg': 'hometurffortworth.com/public/images/locations/north-richland-hills-tx-commercial-artificial-turf-installation.jpg',
  'denton-tx.jpg': 'artificialgrassflowermound.com/public/images/locations/denton-tx-premium-artificial-grass-installation.jpg',
  'flower-mound-tx.webp': 'artificialgrassflowermound.com/public/images/locations/flower-mound-tx-premium-artificial-grass-installation.webp',
  'allen-tx.jpg': 'artificialgrasssugarland.com/public/images/locations/allen-tx-artificial-turf-installation.jpg',
};

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyLocationImages() {
  const outDir = path.join(project, 'public', 'images', 'locations');
  ensureDir(outDir);
  for (const stale of ['grand-prairie-tx.jpg']) {
    fs.rmSync(path.join(outDir, stale), { force: true });
  }
  for (const [fileName, sourceRel] of Object.entries(locationImageSources)) {
    const source = path.join(turfRoot, sourceRel);
    if (!fs.existsSync(source)) {
      console.warn(`Missing location image source: ${sourceRel}`);
      continue;
    }
    fs.copyFileSync(source, path.join(outDir, fileName));
  }
}

function slugTitle(slug) {
  return slug.split('-').map((part) => part.charAt(0).toUpperCase() + part.slice(1)).join(' ');
}

function paragraphs(lines) {
  return lines.map((line) => `<p>${line}</p>`).join('\n');
}

function linksFor(tax, selfSlug, count = 8) {
  const pools = {
    services: serviceItems.map((item) => ({ taxonomy: 'services', slug: item.slug, anchor: item.name })),
    'building-types': buildingTypeItems.map(([slug, name]) => ({ taxonomy: 'building-types', slug, anchor: name })),
    industries: industryItems.map(([slug, name]) => ({ taxonomy: 'industries', slug, anchor: name })),
    locations: locationItems.map(([slug, name]) => ({ taxonomy: 'locations', slug, anchor: name })),
  };
  const order = [];
  const groups = [pools[tax] || [], pools.services, pools['building-types'], pools.industries, pools.locations];
  for (const group of groups) {
    for (const item of group) order.push(item);
  }
  const seen = new Set();
  const out = [];
  for (const item of order) {
    const key = `${item.taxonomy}/${item.slug}`;
    if (item.slug === selfSlug || seen.has(key)) continue;
    seen.add(key);
    out.push(item);
    if (out.length >= count) break;
  }
  return out;
}

function serviceContent(item) {
  return [
    {
      heading: 'Scope That Matches The Space',
      html: paragraphs([
        `A ${item.name.toLowerCase()} scope from ${bizName} starts with the way the space has to operate, not with a generic list of construction tasks. The first review looks at access, existing utilities, walls, ceiling heights, equipment locations, finish expectations, and the schedule pressure around the project. That matters in ${region}, where commercial and residential properties often combine older utility conditions with new equipment demands and tight owner timelines.`,
        item.detail,
        `The work is planned around ${item.use}. When those details are reviewed together, the project has a cleaner path through demolition, rough-in, inspections, finishes, and closeout. Owners get a scope that explains what is included, what needs field verification, and which decisions have to be made before crews start opening walls or ceilings.`,
      ]),
    },
    {
      heading: 'How The Work Is Sequenced',
      html: paragraphs([
        `Strong ${item.name.toLowerCase()} work is built in the right order. Extreme Buildouts LLC confirms the existing condition, identifies trade conflicts, prices the work in phases when needed, and builds a schedule around the parts of the property that cannot be interrupted. That sequence keeps the job from turning into disconnected trade visits with no clear finish line.`,
        `Mechanical, electrical, plumbing, framing, finish carpentry, fixtures, paint, flooring, and punch items all affect each other. A late change in one area can move inspections, delay finish work, or create visible compromises. The project plan is written so rough work supports finish work, and finish work supports the way the owner needs to use the space.`,
        `For ${item.angle}, that coordination is the difference between a buildout that looks complete and one that still has open items after turnover. The goal is not to create a longer process; it is to make the process clear enough that owners know what happens next and crews can keep moving.`,
      ]),
    },
    {
      heading: 'Built For Texas Conditions',
      html: paragraphs([
        `${region} construction has its own practical constraints. Heat, humidity, storm windows, long material runs, rural service access, older building stock, and fast-growing commercial corridors can all affect schedule and cost. Extreme Buildouts LLC plans around those realities instead of pricing the work as if every site were a clean new shell.`,
        `If the project is occupied, the plan accounts for dust, noise, utility interruptions, parking, customer access, and end-of-day cleanup. If the project is vacant, the plan focuses on efficient sequence, trade access, and keeping the finish date realistic. Either way, the scope is tied to field conditions rather than assumptions that fall apart once demolition starts.`,
        `The final deliverable is a usable space. That means the A/C works with the layout, electrical service supports the equipment, plumbing is where the fixtures need it, finishes are complete, and the owner is not left managing unresolved trade gaps after the crew leaves.`,
      ]),
    },
    {
      heading: 'Existing Conditions That Change The Work',
      html: paragraphs([
        `A strong ${item.name.toLowerCase()} plan separates known work from field-verification work before crews mobilize. Existing panels, shutoffs, roof penetrations, above-ceiling space, slab conditions, wall framing, utility chases, and equipment access all need attention because one hidden condition can change the trade sequence.`,
        `Extreme Buildouts LLC documents those risk points in practical language. If a ceiling must be opened before a final route is confirmed, that gets identified. If a water line, drain, panel, or duct path could limit the layout, that gets reviewed before finishes are ordered. Owners get a clearer scope because the plan is built around the property that is actually there.`,
        `That approach matters on smaller jobs as much as larger ones. A short buildout can still be delayed by a missing disconnect, blocked cleanout, overloaded panel, or duct route that conflicts with framing. Early field review keeps those details visible before the schedule depends on them.`,
      ]),
    },
    {
      heading: 'Decisions Owners Should Make Early',
      html: paragraphs([
        `${item.name} work moves faster when owner decisions are made before the field schedule is compressed. Equipment selections, fixture counts, lighting levels, finish standards, restroom changes, access rules, and operating hours all affect cost and timing. Extreme Buildouts LLC brings those decisions forward instead of letting them surface after rough-in starts.`,
        `Some decisions affect more than one trade. A new appliance can require power, plumbing, ventilation, blocking, finish clearance, and inspection planning. A wall shift can affect ceiling layout, return air, outlets, switches, trim, and flooring transitions. The construction scope needs those connections mapped early so the finished work does not feel patched together.`,
        `When a decision is not ready, it can be carried as an allowance, alternate, or field-verification item. That keeps the project honest without freezing progress around details that still need owner input.`,
      ]),
    },
    {
      heading: 'How Pricing And Scheduling Stay Clear',
      html: paragraphs([
        `A useful proposal for ${item.name.toLowerCase()} should explain the trade scope, the finish scope, the assumed schedule, the exclusions, and the items that may change after field review. Extreme Buildouts LLC avoids vague construction language because vague language creates arguments at the worst point in the job.`,
        `The schedule is built around the sequence of work: demolition or prep, rough-in, inspections, close-in, finishes, equipment setting, startup, punch, and cleanup. When the property is occupied, the plan also accounts for shutdowns, temporary access, noisy work, parking, and protection of active areas.`,
        `Owners can use that structure to make decisions before money is spent in the wrong order. The result is a cleaner buildout conversation, tighter trade coordination, and fewer surprises as the project moves toward turnover.`,
      ]),
    },
    {
      heading: 'Closeout That Holds Up After Turnover',
      html: paragraphs([
        `Closeout is not just the final walkthrough. For ${item.name.toLowerCase()}, closeout means the finished space can be used without unresolved trade conflicts, missing access, or visible fixes that should have been solved earlier. Extreme Buildouts LLC checks the work against the intended use of the space, not only against a list of completed tasks.`,
        `That includes device placement, fixture setting, trim transitions, service clearances, equipment startup, cleanup, and the punch items that affect daily use. A space can look close to finished and still fail the owner if the A/C access is blocked, an outlet is missing, a drain is wrong, or the finish work does not match the operating need.`,
        `The closeout goal is a space that opens cleanly, works correctly, and gives the owner confidence that A/C, electrical, plumbing, construction, and finish work were coordinated under one plan.`,
      ]),
    },
  ];
}

function buildingContent(slug, name, needs) {
  return [
    {
      heading: 'Construction Planned Around The Building Type',
      html: paragraphs([
        `${name} require a buildout plan that respects how the property will actually be used. Extreme Buildouts LLC reviews the existing structure, utilities, access, finish expectations, inspection path, and schedule before pricing the work. That early review is especially important for ${needs}.`,
        `A project can look simple until the trades start crossing each other. A wall change can affect duct routing. A new sink can affect slab work. A lighting plan can affect ceiling layout. A new piece of equipment can require dedicated power or ventilation. The buildout plan connects those decisions before work starts so the owner has a clearer path to completion.`,
        `For ${name.toLowerCase()} in ${region}, the work often has to account for heat, humidity, storm timing, existing utility conditions, and material availability. The right construction sequence keeps the project moving without hiding details that should be solved before finishes go in.`,
      ]),
    },
    {
      heading: 'Trade Coordination And Finish Control',
      html: paragraphs([
        `Extreme Buildouts LLC coordinates A/C, electrical, plumbing, framing, drywall, doors, trim, fixtures, flooring, paint, and punch work around the owner priority for the space. Some projects need speed. Some need careful phasing. Some need a durable finish more than a decorative one. The scope should reflect those priorities clearly.`,
        `The team looks at rough-in locations, equipment access, service clearances, shutoff locations, attic or ceiling conditions, drain paths, lighting levels, and where future service calls will happen. Those details are easier to solve before walls are closed and finishes are installed.`,
        `The result is a buildout that can be understood by the owner, the field crew, and anyone approving the spend. Clear inclusions, exclusions, allowances, and field-verification items prevent the misunderstandings that usually show up late in a project.`,
      ]),
    },
    {
      heading: 'A Practical Path To Turnover',
      html: paragraphs([
        `Turnover is more than finishing the visible work. The space has to function, pass the necessary inspections, and be ready for the people who will occupy it. For ${name.toLowerCase()}, that means close attention to final device placement, fixture setting, equipment startup, cleanup, and punch work.`,
        `If the property is active, construction is planned around customers, residents, staff, tenants, or inventory. If it is a new or vacant space, the focus shifts to efficient access, material movement, and keeping crews sequenced without avoidable waiting time.`,
        `Extreme Buildouts LLC keeps the conversation grounded in jobsite reality: what is known, what needs to be opened up, what could change the price, and what has to happen before the space is ready. That is the kind of clarity owners need when a project has real money and a real deadline behind it.`,
      ]),
    },
    {
      heading: 'Early Review Before The Buildout Starts',
      html: paragraphs([
        `The first walk-through for ${name.toLowerCase()} should answer more than whether the space is empty. Extreme Buildouts LLC looks at utility locations, roof or attic access, slab conditions, panel capacity, restrooms, existing equipment, ceiling height, structural limits, and the path materials will take into the property.`,
        `That review helps separate easy finish work from work that requires trade planning. A simple-looking wall change can affect ductwork, lighting, outlets, fire blocking, plumbing, flooring, and trim. A new use can require different ventilation, dedicated circuits, added fixtures, or changes to the way occupants move through the property.`,
        `The owner gets a better scope when those conditions are discussed before crews arrive. Unknowns can be priced as allowances or field-verification items, and known work can be sequenced with fewer late surprises.`,
      ]),
    },
    {
      heading: 'Mechanical, Electrical, And Plumbing Fit',
      html: paragraphs([
        `${name} often fail or succeed in the hidden work: A/C sizing and routing, electrical distribution, plumbing access, equipment clearances, service shutoffs, and inspection timing. Extreme Buildouts LLC treats those details as part of the building plan, not as separate add-ons that get solved after walls are framed.`,
        `The finished space has to be comfortable, serviceable, and ready for the way it will be used. That requires planning for duct paths, returns, drains, vents, water heaters, panels, dedicated circuits, lighting controls, and where future maintenance will happen. These details are easier and cheaper to solve before finishes cover the work.`,
        `When MEP work is coordinated early, finish work can stay cleaner. Floors, ceilings, walls, trim, doors, and paint do not have to be opened again because a trade conflict was missed during rough-in.`,
      ]),
    },
    {
      heading: 'Budget Discipline Without Cutting The Wrong Corners',
      html: paragraphs([
        `Every ${name.toLowerCase()} project has budget pressure, but the wrong shortcut can create bigger costs after turnover. Extreme Buildouts LLC helps owners compare options around scope, phasing, finish level, material choices, trade sequencing, and items that can safely wait without damaging the finished result.`,
        `The budget conversation should identify what must happen for code, safety, comfort, and function before focusing on optional finishes. A less expensive finish can be reasonable. Skipping service access, undersizing infrastructure, hiding a known utility issue, or failing to protect an occupied area usually is not.`,
        `A clear scope gives the owner control. It shows where money is going, what decisions affect cost, and which conditions could change the budget after demolition or utility review.`,
      ]),
    },
    {
      heading: 'Phasing Around People And Operations',
      html: paragraphs([
        `${name} may involve tenants, customers, residents, staff, vendors, inspectors, or neighboring properties. Extreme Buildouts LLC plans around those people as part of the construction sequence. Access, noise, dust, parking, deliveries, temporary shutdowns, and end-of-day cleanup can affect whether the project feels controlled or chaotic.`,
        `Some projects need night or off-hour work. Others need a clean break between rough construction and finish installation. Residential work may need temporary utility planning. Commercial work may need landlord communication, inspection windows, or careful turnover around an opening date.`,
        `Phasing is most useful when it is written into the scope instead of improvised. Clear phases help owners understand what areas will be affected, when decisions are due, and how the work moves from rough conditions to a usable finished space.`,
      ]),
    },
    {
      heading: 'Final Checks Before The Space Is Used',
      html: paragraphs([
        `The final review for ${name.toLowerCase()} connects the original scope to the finished condition. Extreme Buildouts LLC checks the visible finish work, the hidden trade work that supports it, the access needed for future service, and the punch items that affect daily use.`,
        `That review can include A/C startup, electrical device placement, fixture setting, door and hardware operation, flooring transitions, paint touchups, equipment access, cleanup, and owner walkthrough items. A clean closeout reduces the chance that the owner has to chase small trade gaps after moving in.`,
      ]),
    },
  ];
}

function industryContent(slug, name, needs) {
  return [
    {
      heading: 'Construction Support For The Way You Operate',
      html: paragraphs([
        `${name} need construction scopes that fit business decisions, not just building conditions. Extreme Buildouts LLC starts by reviewing the property, intended use, timeline, access limits, utility needs, and the points where A/C, electrical, plumbing, and finish work have to connect. That is important for ${needs}.`,
        `A vague estimate can create problems once the work reaches rough-in. The better approach is to identify the likely constraints early: existing service capacity, slab or wall conditions, equipment requirements, inspection sequence, material selections, and owner decisions that affect the schedule.`,
        `The work is then organized into a practical construction path. Owners can see what needs immediate action, what should be decided before materials are ordered, and which items should be priced as alternates because the field condition is not confirmed yet.`,
      ]),
    },
    {
      heading: 'In-House Trade Coordination',
      html: paragraphs([
        `A/C, electrical, plumbing, and construction work should not be planned in separate conversations when the space has to open on a schedule. Extreme Buildouts LLC coordinates those scopes together so the finished space does not carry the marks of trade gaps: exposed fixes, misplaced devices, blocked access, or finish work that has to be reopened.`,
        `That matters for ${name.toLowerCase()} because downtime, tenant frustration, customer disruption, or resident inconvenience can cost more than the construction item itself. The project plan accounts for access, staging, cleanup, utility interruptions, and end-of-day protection before crews arrive.`,
        `When the job is larger, the scope can be broken into phases with clear decision points. When the job is smaller, the same discipline keeps repairs and improvements from growing into an unmanaged list of side work.`,
      ]),
    },
    {
      heading: 'Clear Scope Before Crews Mobilize',
      html: paragraphs([
        `Extreme Buildouts LLC documents the work in plain language: what will be built, what trade work is included, what finish level is expected, what conditions could change the price, and what schedule assumptions are being used. That clarity helps owners compare options and approve work without guessing what is missing.`,
        `For ${name.toLowerCase()}, the best construction plan is usually the one that acknowledges the property realities early. Older buildings may need utility correction. New shells may need complete rough-in. Occupied spaces may need phasing. Rural projects may need material and crew logistics planned more tightly.`,
        `The goal is a finished space that works for the owner after the crew leaves. That means comfortable air, reliable power, working plumbing, durable finishes, clean transitions, and a closeout process that does not leave unresolved trade items behind.`,
      ]),
    },
    {
      heading: 'What Gets Reviewed Before Pricing',
      html: paragraphs([
        `${name} need pricing that reflects the building, the schedule, and the operational pressure behind the work. Extreme Buildouts LLC reviews existing conditions, utility capacity, access, equipment needs, finish expectations, required inspections, and the places where one trade can block another.`,
        `That review is practical. A restaurant operator needs ventilation, plumbing, power, equipment placement, and health-related details considered together. A landlord may need a suite cleaned up quickly without creating a future maintenance issue. A homeowner may need trade upgrades without losing use of the house for longer than necessary.`,
        `When pricing starts with those realities, the scope becomes easier to understand. Owners can see which work is required, which choices are discretionary, and what needs to be verified in the field before final decisions are made.`,
      ]),
    },
    {
      heading: 'Budget, Phasing, And Downtime',
      html: paragraphs([
        `Downtime is a real cost for ${name.toLowerCase()}. A buildout that saves money on paper can still be expensive if it disrupts operations, delays turnover, or requires finished work to be reopened. Extreme Buildouts LLC builds the sequence around the property use so the construction plan supports the business or household using the space.`,
        `The scope can identify phases for demolition, rough-in, inspections, finish work, equipment setting, and punch items. It can also separate immediate work from alternates when the owner needs budget control. That gives owners a way to make decisions without losing sight of the work that must happen first.`,
        `Clear phasing also helps field crews. Everyone understands which areas are active, what has to stay protected, when utilities may be interrupted, and what has to be complete before the next trade begins.`,
      ]),
    },
    {
      heading: 'Construction Details That Protect The Finished Space',
      html: paragraphs([
        `${name} usually care most about the finished result, but the quality of that result is decided during rough construction. Framing, blocking, duct routes, drains, vents, panel loads, lighting controls, material transitions, and service access all shape how the finished space performs.`,
        `Extreme Buildouts LLC pays attention to those details before finish materials are installed. That reduces the chance of visible surface fixes, poor access, awkward equipment placement, or repairs that should have been avoided during planning.`,
        `The work is organized so the finished space can be used, maintained, and adjusted over time. That kind of planning is especially important when owners are investing in a space they expect to operate from every day.`,
      ]),
    },
    {
      heading: 'One Responsible Construction Conversation',
      html: paragraphs([
        `A disconnected handoff between trades creates confusion for ${name.toLowerCase()}. One contractor may assume another contractor is handling access, rough-in, cleanup, protection, inspection timing, or final device placement. Extreme Buildouts LLC keeps A/C, electrical, plumbing, and construction work in one coordinated conversation.`,
        `That does not remove every unknown condition, but it makes unknowns easier to manage. When a field issue appears, the decision can be made with the full construction sequence in mind instead of solving one trade problem while creating another.`,
        `The owner gets a clearer point of contact, a tighter scope, and a better chance of reaching turnover without a pile of unresolved trade questions left behind.`,
      ]),
    },
    {
      heading: 'Closeout That Supports The Next Use',
      html: paragraphs([
        `Closeout for ${name.toLowerCase()} should support the next day of use, not just the last day of construction. Extreme Buildouts LLC reviews comfort, power, plumbing, finishes, service access, cleanup, punch items, and owner questions before the work is treated as complete.`,
        `That matters when a tenant is moving in, a restaurant is preparing equipment, a property owner is showing a suite, a facility manager is reopening an area, or a homeowner is returning to normal routines. The finished space should be ready for that next step without unresolved trade gaps slowing it down.`,
      ]),
    },
  ];
}

function locationContent(slug, name, local) {
  return [
    {
      heading: `Buildout Work In ${name}`,
      html: paragraphs([
        `${bizName} serves ${name} with commercial and residential construction, retail buildouts, A/C, electrical, plumbing, design-build planning, renovations, and ground-up work. Projects in this area are shaped by ${local}, so the construction plan has to be practical from the first site walk.`,
        `The first review looks at access, utilities, existing conditions, schedule pressure, finish expectations, and the point where the owner needs the space to be usable. That creates a better scope than pricing only the visible work and discovering the trade conflicts later.`,
        `For ${name} owners, the value is coordination. A/C, electrical, plumbing, framing, finishes, and punch work are planned together so the project has one path from rough-in through closeout.`,
      ]),
    },
    {
      heading: 'Commercial And Residential Scope Control',
      html: paragraphs([
        `Commercial work in ${name} often depends on opening dates, landlord rules, tenant coordination, equipment needs, and inspections. Residential work often depends on access, dust control, utility interruptions, and keeping the home functional while work is underway. Extreme Buildouts LLC plans those details before crews arrive.`,
        `Retail suites, offices, restaurants, homes, and light commercial spaces each need a different sequence. Some require heavy rough-in before finishes. Some require careful phasing around occupants. Some need early decisions on equipment, fixtures, and lighting so the rest of the work can move cleanly.`,
        `The scope is written to keep owner decisions visible: what is included, what is excluded, what needs field verification, and what could change after demolition or utility review. That helps the project move without burying important details in vague language.`,
      ]),
    },
    {
      heading: 'Texas Field Conditions',
      html: paragraphs([
        `${region} work has to account for heat, humidity, storm timing, soil movement, older structures, rural access, and long material runs. In ${name}, those details can affect everything from scheduling to A/C performance to how plumbing and electrical work are routed through an existing building.`,
        `Extreme Buildouts LLC keeps the project grounded in field conditions. If the existing building needs correction before finish work, that gets documented. If the schedule depends on a permit, inspection, special material, or equipment delivery, that gets called out before the owner commits to a finish date.`,
        `The end goal is simple: a finished space that works. Comfortable air, reliable electrical, working plumbing, clean finishes, and a closeout process that leaves the owner with a usable commercial or residential property.`,
      ]),
    },
    {
      heading: 'Local Planning Factors',
      html: paragraphs([
        `${name} projects need a scope that respects the local market instead of treating every property like the same clean shell. Existing buildings may have older panels, limited ceiling space, patched plumbing, roof access issues, slab surprises, or finish conditions that affect the buildout. Newer spaces can still have landlord rules, incomplete utility information, or equipment needs that change the plan.`,
        `The local conditions around ${local} make early planning important. Extreme Buildouts LLC reviews parking, access, delivery routes, utility shutoff points, nearby occupied areas, inspection timing, and the owner deadline before the sequence is set. That keeps the project grounded in what the field crew will actually face.`,
        `A good scope also protects the owner from assumptions. If a condition needs to be opened, measured, tested, or verified, it should be called out before crews start depending on it. That makes the construction conversation clearer and helps avoid change orders that come from preventable blind spots.`,
      ]),
    },
    {
      heading: 'Commercial Buildouts That Fit The Market',
      html: paragraphs([
        `Commercial construction in ${name} can include retail finish-outs, restaurant work, medical and office suites, warehouse support areas, light industrial improvements, shell-to-finish projects, and renovations inside active buildings. Each use creates different pressure on A/C, electrical, plumbing, layout, finishes, and inspections.`,
        `Retail and restaurant spaces often need quick opening schedules, public-facing finishes, lighting decisions, signage coordination, restroom planning, and equipment rough-ins. Office and medical spaces need clean circulation, comfort, privacy, durable finishes, and reliable power. Warehouse and industrial-adjacent spaces need equipment access, ventilation, durable surfaces, and practical utility routing.`,
        `Extreme Buildouts LLC builds the scope around the intended use. That means the trade plan supports the way people will move through the space, where equipment will sit, how utilities will be serviced, and what has to be complete before the owner can open or occupy the property.`,
      ]),
    },
    {
      heading: 'Residential Remodeling And Additions',
      html: paragraphs([
        `Residential work in ${name} needs a different kind of planning because the project often happens around daily life. Kitchens, bathrooms, additions, garage conversions, utility upgrades, HVAC changes, and finish renovations can all affect access, dust control, parking, family schedules, and temporary utility interruptions.`,
        `Extreme Buildouts LLC reviews how the house is currently built before committing to the construction sequence. Framing, attic access, slab conditions, drain locations, panel capacity, duct routing, roofline changes, and finish transitions all matter when a remodel or addition has to feel like it belongs to the existing home.`,
        `The goal is to keep the owner informed without turning the project into a daily guessing game. Clear phases, clear decisions, and clear cleanup expectations make residential work easier to live through and easier to finish correctly.`,
      ]),
    },
    {
      heading: 'MEP Coordination Before Finishes',
      html: paragraphs([
        `A/C, electrical, and plumbing decisions should be made before the finish schedule takes over. In ${name}, that means checking load needs, duct paths, equipment access, circuit requirements, lighting placement, fixture locations, drain and vent routing, shutoffs, water heater placement, and inspection windows early enough to adjust the layout if needed.`,
        `When trade work is treated as separate side work, the finished space usually shows it. Surface fixes, awkward access panels, misaligned fixtures, missing outlets, poor comfort, or blocked service areas are often the result of decisions made too late. Extreme Buildouts LLC coordinates those trades as part of the buildout plan.`,
        `That coordination is especially important for commercial spaces changing use, restaurants adding equipment, offices adding rooms, homes adding conditioned space, and older buildings where existing systems may not match the new plan.`,
      ]),
    },
    {
      heading: 'Scope, Budget, And Closeout',
      html: paragraphs([
        `A construction scope in ${name} should explain what is included, what is excluded, what needs owner selection, what depends on field verification, and what schedule assumptions are being used. Extreme Buildouts LLC keeps those details visible because hidden assumptions are where budget problems usually start.`,
        `The budget can be organized around required work, finish choices, alternates, and items that may wait for a later phase. That gives owners a way to make decisions without cutting the work that protects function, service access, comfort, or code compliance.`,
        `Closeout is handled with the same discipline. The finished space should have working A/C, reliable power, completed plumbing, clean finishes, accessible equipment, and punch items resolved before the owner is left to manage the aftermath. That is the difference between a buildout that merely looks done and a project that is ready to use.`,
      ]),
    },
  ];
}

function faqsFor(name, taxonomy = '') {
  const label = taxonomy === 'locations' ? `work in ${name}` : name.toLowerCase();
  return [
    {
      q: `What information helps ${bizName} review ${label}?`,
      a: `<p>Photos, the project address or area, desired use of the space, timing, known utility needs, existing plans, landlord rules, and a rough budget range all help the first review. A site walk is still needed before final scope and pricing.</p>`,
    },
    {
      q: `Can A/C, electrical, and plumbing be included with ${label}?`,
      a: `<p>Yes. Extreme Buildouts LLC coordinates A/C, electrical, plumbing, and construction work together so the project is not split into disconnected trade scopes.</p>`,
    },
    {
      q: `How are unknown conditions handled on ${label}?`,
      a: `<p>Unknown conditions are identified as field-verification items before work starts. If demolition or utility review reveals something different, the scope can be adjusted with the owner before finish work hides the issue.</p>`,
    },
  ];
}

function writeItem(taxonomy, slug, name, metaDescription, sections, faqs = faqsFor(name, taxonomy)) {
  const dir = path.join(project, taxonomy);
  ensureDir(dir);
  const item = {
    slug,
    taxonomy,
    route: `/${taxonomy}/${slug}`,
    name,
    title: `${name} | ${bizName}`,
    metaDescription,
    internalLinks: linksFor(taxonomy, slug),
    sections,
    faqs,
  };
  fs.writeFileSync(path.join(dir, `${slug}.json`), `${JSON.stringify(item, null, 2)}\n`);
}

ensureDir(project);
ensureDir(path.join(project, 'data'));
ensureDir(path.join(project, 'scripts'));
copyLocationImages();

fs.writeFileSync(path.join(project, 'home.config.json'), `${JSON.stringify({
  domain: 'extremebuildouts.com',
  clone_dir: project,
  content_dir: project,
  reference: 'https://extremebuildouts.com/',
  refhost: 'extreme-reference',
  biz: bizName,
  wordmark_l1: 'Extreme',
  wordmark_l2: 'Buildouts LLC',
  city: region,
  region,
  phone: '',
  email: 'hello@extremebuildouts.com',
  hero_image: '/ours/building-types/retail-stores-shopping-centers.jpg',
  nav: [
    ['Services', '/services'],
    ['Project Types', '/building-types'],
    ['Industries', '/industries'],
    ['Service Areas', '/locations'],
    ['About', '/about'],
    ['Contact', '/contact'],
  ],
  cta: ['Request a Buildout Review', '/contact'],
}, null, 2)}\n`);

fs.writeFileSync(path.join(project, 'data', 'biz-info.json'), `${JSON.stringify({
  businessName: bizName,
  name: bizName,
  city: region,
  region,
  phone: '',
  email: 'hello@extremebuildouts.com',
  domain: 'extremebuildouts.com',
}, null, 2)}\n`);

fs.writeFileSync(path.join(project, 'data', 'priority.json'), `${JSON.stringify({
  services: serviceItems.map((item) => item.slug),
  'building-types': buildingTypeItems.map(([slug]) => slug),
  industries: industryItems.map(([slug]) => slug),
  locations: locationItems.map(([slug]) => slug),
}, null, 2)}\n`);

for (const item of serviceItems) {
  writeItem(
    'services',
    item.slug,
    item.name,
    `${item.name} from ${bizName}: coordinated construction, A/C, electrical, plumbing, finish-out, and buildout planning across ${region}.`,
    serviceContent(item),
    item.faqs.map(([q, a]) => ({ q, a: `<p>${a}</p>` })),
  );
}

for (const [slug, name, needs] of buildingTypeItems) {
  writeItem(
    'building-types',
    slug,
    name,
    `${name} built out by ${bizName} with coordinated construction, A/C, electrical, plumbing, finishes, and turnover planning across ${region}.`,
    buildingContent(slug, name, needs),
  );
}

for (const [slug, name, needs] of industryItems) {
  writeItem(
    'industries',
    slug,
    name,
    `${name} use ${bizName} for coordinated buildouts, renovations, A/C, electrical, plumbing, and construction work across ${region}.`,
    industryContent(slug, name, needs),
  );
}

for (const [slug, name, local] of locationItems) {
  writeItem(
    'locations',
    slug,
    name,
    `${bizName} serves ${name} with commercial and residential construction, retail buildouts, A/C, electrical, plumbing, and design-build work.`,
    locationContent(slug, name, local),
  );
}

console.log(`Wrote Extreme Buildouts content to ${project}`);
console.log(`Counts: ${serviceItems.length} services, ${buildingTypeItems.length} project types, ${industryItems.length} industries, ${locationItems.length} service areas`);
