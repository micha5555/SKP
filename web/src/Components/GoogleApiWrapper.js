import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';


const customIcon = L.icon({
  iconUrl: '/icon.png',
  iconSize: [32, 32], // size of the icon
  iconAnchor: [16, 32], // point of the icon which will correspond to marker's location
});

const Map = ({center}) => {
  const location = [52.23268300909039, 21.012947238290486]; // Replace with your specific location coordinates

  return (
    <MapContainer className='mb-3' center={location} zoom={16} scrollWheelZoom={false} style={{height: '300px', borderRadius: '20px'}}>
      {console.log(center)}
      <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={location} icon={customIcon}>
      </Marker>
    </MapContainer>
  );
};

export default Map;
