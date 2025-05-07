// Define width and height for the SVG map
const width = 800;
const height = 600;

// Create SVG container
const svg = d3.select("#map")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

// Define projection and path generator
const projection = d3.geoMercator()
  .center([-73.94, 40.70]) // Center on NYC
  .scale(40000)            // Zoom level
  .translate([width / 2, height / 2]);

const path = d3.geoPath().projection(projection);

// Save original full map viewBox
let originalViewBox = `0 0 ${width} ${height}`;

// Load NYC Borough GeoJSON data
d3.json("/static/data/nyc_boroughs.geojson").then(function(geojson) {
  // Draw borough shapes
  svg.selectAll("path")
    .data(geojson.features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("fill", "#87CEEB")
    .attr("stroke", "#333")
    .attr("stroke-width", 1)
    .on("mouseover", function () {
      d3.select(this).attr("fill", "#ffa07a"); // Highlight borough on hover
    })
    .on("mouseout", function () {
      d3.select(this).attr("fill", "#87CEEB"); // Reset borough color
    })
    .on("click", function(event, d) {
      zoomToBorough(d);
      loadDishes(d.properties.name); // d.properties.name should match borough name
      $("#reset-btn").show();
    });

  // Draw borough labels
  svg.selectAll("text")
    .data(geojson.features)
    .enter()
    .append("text")
    .attr("x", d => path.centroid(d)[0])
    .attr("y", d => path.centroid(d)[1])
    .text(d => d.properties.name)
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .style("font-family", "Arial")
    .style("font-size", "14px")
    .style("font-weight", "bold")
    .style("fill", "#2c3e50")
    .style("pointer-events", "none")
    .style("text-shadow", "1px 1px 2px white");
});

// Zoom into the clicked borough
function zoomToBorough(d) {
  const [[x0, y0], [x1, y1]] = path.bounds(d);
  svg.transition()
    .duration(1000)
    .attr("viewBox", `${x0} ${y0} ${x1 - x0} ${y1 - y0}`);
}

// Load dishes dynamically for the selected borough
function loadDishes(borough) {
  $.getJSON(`/get_borough/${borough}`, function(dishes) {
    let html = `
        <h1 class="text-primary">${borough}</h1>
    `;

    dishes.forEach(dish => {
      const imageSrc = dish.image.startsWith('http') ? dish.image : `/static/images/${dish.image}`;

      html += `
        <div class="col-md-4 mb-4">
          <div class="flip-card" style="cursor:pointer;">
            <div class="flip-card-inner">
              <div class="flip-card-front">
                <img src="${imageSrc}" alt="${dish.name}" class="img-fluid" style="width:100%; height:300px; object-fit:cover;">
              </div>
              <div class="flip-card-back">
                <h5>${dish.name}</h5>
                <p>${dish.description}</p>
              </div>
            </div>
          </div>
        </div>
      `;
    });

    $('#borough-dishes').hide().html(html).fadeIn(500);
    attachFlipListeners(); // Reattach flip click event
  });
}


// Attach flipping functionality
function attachFlipListeners() {
  document.querySelectorAll('.flip-card').forEach(card => {
    card.addEventListener('click', () => {
      card.classList.toggle('flipped');
    });
  });
}

// Reset the map view to full NYC
$("#reset-btn").click(function() {
  svg.transition()
    .duration(1000)
    .attr("viewBox", originalViewBox);

  $("#borough-dishes").fadeOut(300, function() {
    $(this).empty();
  });

  $(this).hide();
});