async function cargar() {
  const estado = document.getElementById("estado");
  estado.textContent = "Cargando...";

  const r = await fetch("/recordatorios/pendientes");
  const data = await r.json();

  const lista = document.getElementById("lista");
  const vacio = document.getElementById("vacio");
  const contador = document.getElementById("contador");

  lista.innerHTML = "";

  const tareas = data.tareas || [];
  contador.textContent = String(tareas.length);

  if (tareas.length === 0) {
    vacio.style.display = "block";
  } else {
    vacio.style.display = "none";
    tareas.forEach(x => {
      const li = document.createElement("li");
      li.className = "item";

      const tarea = document.createElement("div");
      tarea.className = "tarea";
      tarea.textContent = x.tarea ?? String(x);

      const fecha = document.createElement("div");
      fecha.className = "fecha";
      fecha.textContent = x.fecha_creacion ? `Creado: ${x.fecha_creacion}` : "";

      li.appendChild(tarea);
      li.appendChild(fecha);
      lista.appendChild(li);
    });
  }

  estado.textContent = data.mensaje || "Listo.";
}

async function enviar() {
  const input = document.getElementById("mensaje");
  const estado = document.getElementById("estado");
  const mensaje = input.value.trim();

  if (!mensaje) {
    estado.textContent = "Escribe algo primero.";
    return;
  }

  estado.textContent = "Enviando...";

  const r = await fetch("/asistente", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({mensaje})
  });

  const data = await r.json();
  estado.textContent = data.mensaje || "Listo.";

  input.value = "";
  await cargar();
}

document.getElementById("btnEnviar").addEventListener("click", enviar);
document.getElementById("btnRefrescar").addEventListener("click", cargar);
document.getElementById("mensaje").addEventListener("keydown", (e) => {
  if (e.key === "Enter") enviar();
});

cargar();
