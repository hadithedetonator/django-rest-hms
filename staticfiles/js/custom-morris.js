(function ($) {
  "use strict"; // Start of use strict

  // Fetch and render line chart for appointments
  $.getJSON('/api/appointments/', function(data) {
    new Morris.Line({
      element: 'lineMorris',
      resize: true,
      data: data,
      xkey: 'appointment_date',
      ykeys: ['count'],
      labels: ['Appointments'],
      gridLineColor: '#eef0f2',
      lineColors: ['#E57498'],
      lineWidth: 2,
      hideHover: 'auto'
    });
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

    Morris.Donut({
      element: 'donutMorris',
      data: paymentData,
      barSize: 0.1,
      labelColor: '#3e5569',
      resize: true, //defaulted to true
      colors: ['#FFAA2A', '#ef6e6e', '#22c6ab']
    });
  });

  // Fetch and render visit chart for room allotments
  $.getJSON('/api/room-allotments/', function(data) {
    Morris.Area({
      element: 'visitMorris',
      data: data,
      xkey: 'allotment_date',
      ykeys: ['room_number'],
      labels: ['Room Number'],
      pointSize: 0,
      fillOpacity: 1,
      pointStrokeColors: ['#5867c3'],
      behaveLikeLine: true,
      gridLineColor: '#e0e0e0',
      lineWidth: 0,
      smooth: false,
      hideHover: 'auto',
      lineColors: ['#5867c3'],
      resize: true
    });
  });

})(jQuery);
