
const passenger = document.getElementById("passenger");

// Connexion WebSocket avec FastAPI
const ws = new WebSocket("ws://127.0.0.1:8000/ws");

console.log("SmartNav Dashboard started");

ws.onopen = () => {
    console.log("WebSocket connected!");

    document.getElementById("connection").textContent = "Connected";
    document.getElementById("connection").style.color = "#16a34a";
};

ws.onmessage = (event) => {

    console.log("Raw message:", event.data);

    try {

        const data = JSON.parse(event.data);

        console.log("Received data:", data);

        // Le backend envoie x et y directement
        if (data.x === undefined || data.y === undefined) {
            console.warn("Position coordinates missing");
            return;
        }

        const x = Number(data.x);
        const y = Number(data.y);

        // Conversion des coordonnées en pourcentage
        const left = Math.max(0, Math.min(100, (x / 500) * 100));
        const top = Math.max(0, Math.min(100, (y / 400) * 100));

        // Déplacement du passager
        passenger.style.left = left + "%";
        passenger.style.top = top + "%";

        // Informations du passager
        document.getElementById("userId").textContent =
            data.user_id || "--";

        document.getElementById("positionX").textContent = x;

        document.getElementById("positionY").textContent = y;

        document.getElementById("nearestAnchor").textContent =
            data.anchor_id || "--";

        document.getElementById("method").textContent =
            data.method || "--";

        document.getElementById("passengerCount").textContent = "1";

        document.getElementById("lastUpdate").textContent =
            new Date().toLocaleTimeString();

    } catch (error) {

        console.error("JSON processing error:", error);
    }
};

ws.onerror = (error) => {

    console.error("WebSocket error:", error);

    document.getElementById("connection").textContent =
        "Connection error";
};

ws.onclose = () => {

    console.warn("WebSocket disconnected");

    document.getElementById("connection").textContent =
        "Disconnected";
};
