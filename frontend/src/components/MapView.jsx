import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const markers = [
  { position: [51.505, -0.09], label: "London" },
  { position: [40.7128, -74.006], label: "New York" },
  { position: [35.6895, 139.6917], label: "Tokyo" }
];

const MapView = () => (
  <div style={{ height: "400px", marginTop: "40px" }}>
    <h3>Requests Per Country</h3>
    <MapContainer center={[20, 0]} zoom={2} style={{ height: "100%" }}>
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {markers.map((m, i) => (
        <Marker key={i} position={m.position}>
          <Popup>{m.label}</Popup>
        </Marker>
      ))}
    </MapContainer>
  </div>
);

export default MapView;
