import {} from "./d3.v6.js";

  // set the dimensions and margins of the graph
  const margin = {top: 0, right: 30, bottom: 100, left: 60},
      width = 460 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;
  
  // append the svg object to the body of the page
  const svg = d3.select("#graph1")
    .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);
  
  // Parse the Data

  const items = json3
  const replacer = (key, value) => value === null ? '' : value // specify how you want to handle null values here
  const header = Object.keys(items[0])
  var data1 = [
  header.join(','), // header row first
  ...items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
].join('\r\n')
// var data2 = csvToArray(data1);
console.log(data1)

var data = d3.csvParse(data1);

console.log(data)

  // X axis
  const x = d3.scaleBand()
    .range([ 0, width ])
    .domain(data.map(d => d.Info1))
    .padding(0.2);
  svg.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
      .attr("transform", "translate(-10,0)rotate(-45)")
      .style("text-anchor", "end");

  // Add Y axis
  const y = d3.scaleLinear()
    .domain([0, maxpercent])
    .range([ height, 0]);
  svg.append("g")
    .call(d3.axisLeft(y));
  
  svg.append('text')
    .attr('x', -150)
    .attr('y', -35)
    .attr('transform', 'rotate(-90)')
    .attr('text-anchor', 'middle')
    .text('10 Most identified (%)')
  
  // Bars
  svg.selectAll("mybar")
    .data(data)
    .join("rect")
      .attr("x", d => x(d.Info1))
      .attr("y", d => y(d.Info2))
      .attr("width", x.bandwidth())
      .attr("height", d => height - y(d.Info2))
      .attr("fill", "#69b3a2")
  
