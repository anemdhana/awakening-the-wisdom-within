const fs = require('fs');
const html = fs.readFileSync('c:/Users/dhana/GitHub/pssm-swadhyaya-notes/index.html', 'utf8');
const js = fs.readFileSync('c:/Users/dhana/GitHub/pssm-swadhyaya-notes/data/catalog.js', 'utf8');
const results = [
  ['META maitri', html.includes('title: "Maitri Bodh"')],
  ['ORG maitri visible', html.includes('maitri: {') && html.includes('visibleSections: ["maitri"]')],
  ['Sidebar maitri item', html.includes('data-section="maitri"')],
  ['Catalog maitri', js.includes("window.PSSM_CATALOG['maitri']")],
  ['Catalog local URL', js.includes('Spiritual%20Discourses/maitreya-urgency-of-transformation.html')]
];
for (const [name, ok] of results) console.log(name + ':' + ok);
