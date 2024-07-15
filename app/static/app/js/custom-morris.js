(function ($) {
  "use strict"; // Start of use strict

  // Fetch and render line chart for appointments
  $.getJSON('/api/appointments/', function(data) {
    console.log('Data received from API:', data); // Log the received data to the console

    // Helper function to get the quarter from a date
    function getQuarter(date) {
      const month = new Date(date).getMonth() + 1; // getMonth() returns 0-11
      return Math.ceil(month / 3);
    }

    // Aggregate the data by year and quarter
    const aggregatedData = {};
    data.forEach(item => {
      const year = new Date(item.appointment_date).getFullYear();
      const quarter = getQuarter(item.appointment_date);
      const key = `${year} Q${quarter}`;

      if (!aggregatedData[key]) {
        aggregatedData[key] = 0;
      }
      aggregatedData[key]++;
    });

    // Transform aggregated data into the format required by Morris.js
    const formattedData = Object.keys(aggregatedData).map(key => {
      return {
        y: key,
        Appointments: aggregatedData[key]
      };
    });

    console.log('Formatted data for Morris chart:', formattedData); // Log the formatted data to the console

    new Morris.Line({
      element: 'lineMorris',
      resize: true,
      data: formattedData,
      xkey: 'y',
      ykeys: ['Appointments'],
      labels: ['Appointments'],
      gridLineColor: '#eef0f2',
      lineColors: ['#E57498'],
      lineWidth: 2,
      hideHover: 'auto'
    });
  })
  .fail(function(jqxhr, textStatus, error) {
    var err = textStatus + ", " + error;
    console.error("Request Failed: " + err); // Log any error that occurred during the AJAX request
  });

  // Fetch and render bar chart for patients
  $.getJSON('/api/patients/', function(data) {
    new Morris.Bar({
      element: 'barMorris',
      data: data,
      xkey: 'name',
      ykeys: ['age'],
      labels: ['Age'],
      barColors: ['#FF7D00'],
      barOpacity: 1,
      barSizeRatio: 0.5,
      hideHover: 'auto',
      gridLineColor: '#eef0f2',
      resize: true
    });
  });

  // Fetch and render donut chart for payments
  $.getJSON('/api/payments/', function(data) {
    let paymentData = data.map(payment => ({
      label: payment.services,
      value: payment.cost_of_treatment
    }));

    if($("#donutMorris").length == 1){
      // Fetch and render donut chart for appointments
      $.getJSON('/api/appointments/', function(data) {
        console.log('Data received from API:', data); // Log the received data to the console
        
        // Process the data to count the status occurrences
        let statusCounts = data.reduce((acc, appointment) => {
          acc[appointment.status] = (acc[appointment.status] || 0) + 1;
          return acc;
        }, {});

        // Convert the processed data to the format required by Morris Donut chart
        let donutData = Object.keys(statusCounts).map(status => ({
          label: status,
          value: statusCounts[status]
        }));

        console.log('Formatted data for Morris Donut chart:', donutData); // Log the formatted data to the console

        // Render the Morris Donut chart
        Morris.Donut({
          element: 'donutMorris',
          data: donutData,
          barSize: 0.1,
          labelColor: '#3e5569',
          resize: true,
          colors: ['#FFAA2A', '#ef6e6e', '#22c6ab']
        });
      })
      .fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.error("Request Failed: " + err); // Log any error that occurred during the AJAX request
      });
    }
  });

 

})(jQuery);
