import json
import threading

def render_suspense(response, suspense, element_id):

    # send fallback immediately
    response.write(
        f'<div id="{element_id}">{suspense.fallback}</div>'
    )

    def worker():

        tree = suspense.component()
        html = json.dumps(tree)

        script = f"""
<script>
(function(){{
  const root = document.getElementById("{element_id}");
  const tree = {html};

  function createElement(node) {{
      if(typeof node === "string") return node;

      const el = document.createElement(node.type);

      if(node.children){{
          node.children.forEach(c => {{
              el.appendChild(
                  typeof c === "string"
                    ? document.createTextNode(c)
                    : createElement(c)
              );
          }});
      }}

      return el;
  }}

  root.innerHTML = "";
  root.appendChild(createElement(tree));
}})();
</script>
"""
        response.write(script)

    threading.Thread(target=worker).start()