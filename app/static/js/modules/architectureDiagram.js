/**
 * Architecture Showcase interactivity.
 *
 * The node data is embedded server-side as JSON (via Jinja2's |tojson
 * filter, in architecture.html) rather than fetched from an API endpoint.
 * It's the same data on every request and doesn't change per-visitor, so
 * a network round-trip to move it from server to client would be pure
 * overhead — embedding it at render time is the simpler, faster choice.
 * (Contrast with the contact form, which genuinely needs a real POST
 * endpoint, because submitting data *is* a write, not a read.)
 */
export function initArchitectureDiagram() {
  const dataScript = document.getElementById('architecture-data');
  const nodes = document.querySelectorAll('.arch-node');
  if (!dataScript || !nodes.length) return;

  let nodeData;
  try {
    nodeData = JSON.parse(dataScript.textContent);
  } catch {
    return; // Malformed data shouldn't break the rest of the page.
  }

  const byId = Object.fromEntries(nodeData.map((n) => [n.id, n]));

  const layerEl = document.getElementById('arch-detail-layer');
  const labelEl = document.getElementById('arch-detail-label');
  const purposeEl = document.getElementById('arch-detail-purpose');
  const commEl = document.getElementById('arch-detail-comm');
  const whyEl = document.getElementById('arch-detail-why');

  nodes.forEach((node) => {
    node.addEventListener('click', () => selectNode(node.dataset.nodeId));
  });

  function selectNode(id) {
    const info = byId[id];
    if (!info) return;

    nodes.forEach((node) => {
      const isMatch = node.dataset.nodeId === id;
      node.classList.toggle('is-active', isMatch);
      node.setAttribute('aria-pressed', String(isMatch));
    });

    layerEl.textContent = info.layer;
    labelEl.textContent = info.label;
    purposeEl.textContent = info.purpose;
    commEl.textContent = info.communicates_via;
    whyEl.textContent = info.why;
  }
}
