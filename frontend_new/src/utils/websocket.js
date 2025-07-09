let socket;

export const connectWebSocket = (onMessage) => {
  socket = new WebSocket("ws://localhost:8080/ws/metrics");

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onclose = () => {
    console.log("❌ WebSocket closed. Reconnecting...");
    setTimeout(() => connectWebSocket(onMessage), 3000);
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
};

export const disconnectWebSocket = () => {
  if (socket) {
    socket.close();
  }
};
