function createElementFromJSON(node) {
  if (typeof node === "string") return node;

  return React.createElement(
    node.type,
    node.props,
    ...node.children.map(createElementFromJSON)
  );
}

async function loadServerComponent(url) {
  const res = await fetch(url);
  const tree = await res.json();
  return createElementFromJSON(tree);
}