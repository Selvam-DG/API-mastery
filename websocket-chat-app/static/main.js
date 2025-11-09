let ws, me;
    const log = (html, cls="") => {
      const d = document.createElement("div");
      d.className = cls;
      d.innerHTML = html;
      document.getElementById("log").appendChild(d);
      d.scrollIntoView();
    };

    function connect() {
      const u = document.getElementById("username").value.trim();
      const r = document.getElementById("room").value.trim() || "lobby";
      me = u || ("user_" + Math.floor(Math.random()*1000));
      ws = new WebSocket(`ws://${location.host}/ws?username=${encodeURIComponent(me)}&room=${encodeURIComponent(r)}`);
      ws.onopen = () => {
        log(`Connected as <b>${me}</b> to <b>${r}</b>`, "sys");
        document.getElementById("connect").disabled = true;
        document.getElementById("disconnect").disabled = false;
      };
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.type === "system") return log(`🛈 ${msg.text}`, "sys");
          const cls = msg.sender === me ? "me" : "other";
          log(`<b>${msg.sender}:</b> ${msg.text}`, cls);
        } catch (e) { log(`(raw) ${ev.data}`, "sys"); }
      };
      ws.onclose = () => {
        log("Disconnected", "sys");
        document.getElementById("connect").disabled = false;
        document.getElementById("disconnect").disabled = true;
      };
      ws.onerror = (e) => log("Error: " + e?.message, "sys");
    }

    document.getElementById("connect").onclick = connect;
    document.getElementById("disconnect").onclick = () => ws && ws.close();
    document.getElementById("sendForm").onsubmit = (e) => {
      e.preventDefault();
      const text = document.getElementById("text").value.trim();
      if (!text || !ws || ws.readyState !== 1) return;
      ws.send(JSON.stringify({ type: "chat", text }));
      document.getElementById("text").value = "";
    };