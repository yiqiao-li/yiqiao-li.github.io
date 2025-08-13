---
layout: about
title: Home
permalink: /

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p> Dr. Yiqiao Li </p>
    <p> Assistant Professor </p>
    <p> Department of Civil Engineering </p>
    <p> City College of New York </p>
    <p> City University of New York </p>

selected_papers: false # includes a list of papers marked as "selected={true}"
social: false # includes social icons at the bottom of the page

latest_posts:
  enabled: false
  scrollable: true # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

## Welcome

Welcome to the AI & Transportation Research Lab at CCNY! Our lab is dedicated to advancing transportation research by harnessing cutting-edge technologies, including artificial intelligence, advanced sensing systems, and the Internet of Things (IoT). We develop intelligent, data-driven solutions to enhance mobility, safety, and sustainability in transportation systems. Here, you'll find information about our research projects, publications, and opportunities for collaboration.

## Our Mission

Our mission is to push the boundaries of transportation research by leveraging emerging technologies to develop intelligent, data-driven solutions. By focusing on areas such as vehicle classification, mobility analysis, and smart infrastructure, we aim to enhance the efficiency and safety of transportation networks. Through interdisciplinary collaboration and real-world applications, we strive to create impactful innovations that shape the future of mobility.

## Visitor Analytics

<div class="visitor-analytics">
  <div class="visitor-counter">
    <h3>🌍 Global Reach</h3>
    <div class="counter-display">
      <span id="visitor-count">Loading...</span>
      <span class="counter-label">Total Visitors</span>
    </div>
  </div>
  
     <div class="visitor-map">
     <h3>📍 Visitor Locations</h3>
           <div id="map" style="height: 300px; width: 100%; border-radius: 8px; margin: 20px 0; max-width: none;"></div>
     <p class="map-note"><em>This map shows the geographic distribution of our website visitors</em></p>
     <div class="visitor-country-table">
       <h3>Visitor Countries</h3>
       <table id="country-table" class="country-table" style="width:100%; border-collapse: collapse;">
         <thead>
           <tr>
             <th style="text-align:left; padding: 6px 8px; border-bottom: 1px solid #ddd;">Country</th>
             <th style="text-align:right; padding: 6px 8px; border-bottom: 1px solid #ddd;">Visitors</th>
           </tr>
         </thead>
         <tbody></tbody>
       </table>
     </div>
   </div>
</div>

<script>
// Real visitor tracking system
class VisitorTracker {
  constructor() {
    this.visitorCount = 0;
    this.visitorLocations = {};
    // Support resetting analytics via query param: ?resetVisitors=1
    const params = new URLSearchParams(window.location.search);
    this.skipCurrentTrack = params.get('resetVisitors') === '1';
    if (this.skipCurrentTrack) {
      localStorage.removeItem('visitorCount');
      localStorage.removeItem('visitorLocations');
    }
    this.loadData();
    if (!this.skipCurrentTrack) {
      this.trackCurrentVisitor();
    } else {
      // After reset, show zeroed analytics without incrementing
      this.updateDisplay();
      this.updateCountrySummary();
      this.updateCountryTable();
      this.updateMap();
    }
  }

  loadData() {
    // Load visitor count
    this.visitorCount = parseInt(localStorage.getItem('visitorCount') || '0');
    
    // Load visitor locations
    const savedLocations = localStorage.getItem('visitorLocations');
    if (savedLocations) {
      this.visitorLocations = JSON.parse(savedLocations);
    }
  }

  saveData() {
    localStorage.setItem('visitorCount', this.visitorCount.toString());
    localStorage.setItem('visitorLocations', JSON.stringify(this.visitorLocations));
  }

  async trackCurrentVisitor() {
    try {
      // Get visitor's location using IP geolocation
      const response = await fetch('https://ipapi.co/json/');
      const data = await response.json();
      
           if (data.latitude && data.longitude) {
        const locationKey = `${data.latitude.toFixed(2)},${data.longitude.toFixed(2)}`;
             const cityName = `${data.city || 'Unknown'}, ${data.country_name || 'Unknown'}`;
        
        // Update visitor count
        this.visitorCount++;
        
        // Update location data
        if (this.visitorLocations[locationKey]) {
          this.visitorLocations[locationKey].visitors++;
        } else {
               this.visitorLocations[locationKey] = {
            lat: parseFloat(data.latitude),
            lng: parseFloat(data.longitude),
            city: cityName,
                 country: data.country_name || 'Unknown',
            visitors: 1
          };
        }
        
        // Save data
        this.saveData();
        
        // Update display
             this.updateDisplay();
             this.updateCountrySummary();
             this.updateCountryTable();
        this.updateMap();
      }
    } catch (error) {
      console.log('Could not get location, using fallback tracking');
      // Fallback: just increment counter
      this.visitorCount++;
      this.saveData();
           this.updateDisplay();
           this.updateCountrySummary();
           this.updateCountryTable();
      this.updateMap();
    }
  }

  updateDisplay() {
    const countElement = document.getElementById('visitor-count');
    if (countElement) {
      countElement.textContent = this.visitorCount.toLocaleString();
    }
  }

   updateCountrySummary() {
     const summaryEl = document.getElementById('country-summary');
     if (!summaryEl) return;

     // Aggregate visitors by country
     const countryToCount = {};
     Object.values(this.visitorLocations).forEach(loc => {
       const country = (loc.country || (loc.city ? String(loc.city).split(',').slice(-1)[0].trim() : 'Unknown')) || 'Unknown';
       countryToCount[country] = (countryToCount[country] || 0) + (loc.visitors || 0);
     });

     const entries = Object.entries(countryToCount)
       .sort((a, b) => b[1] - a[1])
       .slice(0, 5);

     if (entries.length === 0) {
       summaryEl.textContent = 'Not enough data yet';
       return;
     }

     summaryEl.textContent = entries.map(([country, count]) => `${country} (${count})`).join(', ');
   }

   updateCountryTable() {
     const table = document.getElementById('country-table');
     if (!table) return;
     const tbody = table.querySelector('tbody');
     if (!tbody) return;

     const countryToCount = {};
     Object.values(this.visitorLocations).forEach(loc => {
       const country = (loc.country || (loc.city ? String(loc.city).split(',').slice(-1)[0].trim() : 'Unknown')) || 'Unknown';
       countryToCount[country] = (countryToCount[country] || 0) + (loc.visitors || 0);
     });

     const rows = Object.entries(countryToCount)
       .sort((a, b) => b[1] - a[1])
       .map(([country, count]) => `<tr><td style="padding:6px 8px; border-bottom:1px solid #eee;">${country}</td><td style="padding:6px 8px; text-align:right; border-bottom:1px solid #eee;">${count}</td></tr>`) 
       .join('');

     tbody.innerHTML = rows || '<tr><td colspan="2" style="padding:8px; text-align:center; color:#666;">Not enough data yet</td></tr>';
   }

  updateMap() {
    // Convert visitor locations to array format for map
    const locationsArray = Object.values(this.visitorLocations);
    
    // If no real data yet, show some initial data
    if (locationsArray.length === 0) {
      locationsArray.push({
        lat: 40.7128,
        lng: -74.0060,
        city: 'New York, USA',
        visitors: 1
      });
    }
    
    this.renderMap(locationsArray);
  }

  renderMap(visitorLocations) {
    // Load Leaflet CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(link);
    
    // Load Leaflet JS
    const script = document.createElement('script');
    script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    script.onload = () => {
      // Initialize map
      const map = L.map('map').setView([40.7128, -74.0060], 2);
      
      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);
      
                    // Continuous color scale function based on visitor count
       const getColor = (visitors) => {
         // Define color stops for a smooth gradient
         const colors = [
           { value: 1, color: '#1a9850' },    // Dark green for low traffic
           { value: 5, color: '#91cf60' },    // Green
           { value: 10, color: '#d9ef8b' },   // Light green
           { value: 15, color: '#fee08b' },   // Yellow
           { value: 20, color: '#fc8d59' },   // Orange-red
           { value: 25, color: '#d73027' }    // Dark red for high traffic
         ];
         
         // Find the appropriate color range
         for (let i = 0; i < colors.length - 1; i++) {
           if (visitors >= colors[i].value && visitors < colors[i + 1].value) {
             const ratio = (visitors - colors[i].value) / (colors[i + 1].value - colors[i].value);
             return interpolateColor(colors[i].color, colors[i + 1].color, ratio);
           }
         }
         
         // If visitors >= max value, return the last color
         if (visitors >= colors[colors.length - 1].value) {
           return colors[colors.length - 1].color;
         }
         
         // If visitors < min value, return the first color
         return colors[0].color;
       };
       
       // Helper function to interpolate between two colors
       const interpolateColor = (color1, color2, ratio) => {
         const r1 = parseInt(color1.slice(1, 3), 16);
         const g1 = parseInt(color1.slice(3, 5), 16);
         const b1 = parseInt(color1.slice(5, 7), 16);
         
         const r2 = parseInt(color2.slice(1, 3), 16);
         const g2 = parseInt(color2.slice(3, 5), 16);
         const b2 = parseInt(color2.slice(5, 7), 16);
         
         const r = Math.round(r1 + (r2 - r1) * ratio);
         const g = Math.round(g1 + (g2 - g1) * ratio);
         const b = Math.round(b1 + (b2 - b1) * ratio);
         
         return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
       };
       
       // Add circles for each location with radius and color based on visitor count
       visitorLocations.forEach(location => {
         // Calculate radius based on visitor count (min 5, max 30 pixels)
         const radius = Math.max(5, Math.min(30, location.visitors * 0.6));
         
         // Get color based on visitor count
         const color = getColor(location.visitors);
         
         // Create circle with color scale based on visitor count
         const circle = L.circle([location.lat, location.lng], {
           radius: radius * 1000, // Convert to meters for realistic scale
           color: color,
           fillColor: color,
           fillOpacity: 0.7,
           weight: 2
         }).addTo(map);
         
         // Add popup with visitor information
         circle.bindPopup(`
           <div style="text-align: center;">
             <b>${location.city}</b><br>
             <span style="color: ${color}; font-weight: bold;">${location.visitors} visitors</span><br>
             <small>Color and size indicate visitor count</small>
           </div>
         `);
       });
      
      // Add a special circle for CCNY (larger to represent the lab location)
      const ccnyCircle = L.circle([40.8195, -73.9495], {
        radius: 5000, // 5km radius to make it prominent
        color: '#dc3545',
        fillColor: '#dc3545',
        fillOpacity: 0.8,
        weight: 3
      }).addTo(map);
      
      ccnyCircle.bindPopup(`
        <div style="text-align: center;">
          <b>City College of New York</b><br>
          <span style="color: #dc3545; font-weight: bold;">AI & Transportation Research Lab</span><br>
          <small>Our Research Location</small>
        </div>
      `);
      
                        // Add legend with continuous color bar
        const legend = L.control({position: 'bottomright'});
        legend.onAdd = function(map) {
          const div = L.DomUtil.create('div', 'info legend');
          div.style.backgroundColor = 'white';
          div.style.padding = '10px';
          div.style.borderRadius = '5px';
          div.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
          div.style.fontSize = '12px';
          
          // Create continuous color bar
          const colorBar = document.createElement('div');
          colorBar.style.width = '100%';
          colorBar.style.height = '20px';
          colorBar.style.margin = '10px 0';
          colorBar.style.borderRadius = '3px';
          colorBar.style.background = 'linear-gradient(to right, #1a9850, #91cf60, #d9ef8b, #fee08b, #fc8d59, #d73027)';
          
          // Create color bar labels
          const labels = document.createElement('div');
          labels.style.display = 'flex';
          labels.style.justifyContent = 'space-between';
          labels.style.fontSize = '10px';
          labels.style.color = '#666';
          labels.innerHTML = '<span>1</span><span>5</span><span>10</span><span>15</span><span>20</span><span>25+</span>';
          
          div.innerHTML = `
            <h4 style="margin: 0 0 8px 0; color: #333; font-size: 13px;">Visitor Traffic Heatmap</h4>
            <div style="margin-bottom: 10px;">
              <div style="font-size: 11px; color: #666; margin-bottom: 5px;">Visitors per location:</div>
            </div>
          `;
          
          div.appendChild(colorBar);
          div.appendChild(labels);
          
          // Add CCNY lab location indicator
          const ccnyIndicator = document.createElement('div');
          ccnyIndicator.style.display = 'flex';
          ccnyIndicator.style.alignItems = 'center';
          ccnyIndicator.style.marginTop = '10px';
          ccnyIndicator.style.paddingTop = '10px';
          ccnyIndicator.style.borderTop = '1px solid #eee';
          ccnyIndicator.innerHTML = `
            <div style="width: 12px; height: 12px; background: #dc3545; border-radius: 50%; margin-right: 8px;"></div>
            <span style="font-size: 11px;">CCNY Lab Location</span>
          `;
          div.appendChild(ccnyIndicator);
          
          return div;
        };
      legend.addTo(map);
    };
    document.head.appendChild(script);
  }
}

// Initialize visitor tracking when page loads
document.addEventListener('DOMContentLoaded', function() {
  const tracker = new VisitorTracker();
});
</script>
