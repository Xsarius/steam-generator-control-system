window.onload = function () {
    var dps1 = [];
    var dps2 = [];
    var dps3 = [];
    var dps4 = [];
    var dps5 = [];
    var chart1 = new CanvasJS.Chart("chartContainer1", {
      title: {
        text: "Water tempearature",
      },
      data: [
        {
          type: "line",
          dataPoints: dps1,
        },
      ],
    });

    var chart2 = new CanvasJS.Chart("chartContainer2", {
      title: {
        text: "Steam tempearature (Sensor 1)",
      },
      data: [
        {
          type: "line",
          dataPoints: dps2,
        },
      ],
    });

    var chart3 = new CanvasJS.Chart("chartContainer3", {
      title: {
        text: "Steam tempearature (Sensor 2)",
      },
      data: [
        {
          type: "line",
          dataPoints: dps3,
        },
      ],
    });

    var chart4 = new CanvasJS.Chart("chartContainer4", {
      title: {
        text: "Pressure",
      },
      data: [
        {
          type: "line",
          dataPoints: dps4,
        },
      ],
    });

    var chart5 = new CanvasJS.Chart("chartContainer_pid", {
      title: {
        text: "PID: Control Signal",
      },
      data: [
        {
          type: "line",
          dataPoints: dps5,
        },
      ],
    });

    var updateInterval = 1000;
    var dataLength = 1;

    var xVal1 = 0;
    var yVal1 = 0;
    var updateChart1 = function (count) {
      count = count || 1;

      for (var j = 0; j < count; j++) {
        yVal1 = parseFloat(json_data["water_temp"]);
        dps1.push({
          x: xVal1,
          y: yVal1,
        });
        xVal1++;
      }

      chart1.render();
    };

    var xVal2 = 0;
    var yVal2 = 0;
    var updateChart2 = function (count) {
      count = count || 1;

      for (var j = 0; j < count; j++) {
        yVal2 = (parseFloat(json_data["steam_temp_1"]));
        dps2.push({
          x: xVal2,
          y: yVal2,
        });
        xVal2++;
      }

      chart2.render();
    };

    var xVal3 = 0;
    var yVal3 = 0;
    var updateChart3 = function (count) {
      count = count || 1;

      for (var j = 0; j < count; j++) {
        yVal3 = parseFloat(json_data["steam_temp_2"]);
        dps3.push({
          x: xVal3,
          y: yVal3,
        });
        xVal3++;
      }

      chart3.render();
    };

    var xVal4 = 0;
    var yVal4 = 0;
    var updateChart4 = function (count) {
      count = count || 1;

      for (var j = 0; j < count; j++) {
        yVal4 = parseFloat(json_data["pressure"]);
        dps4.push({
          x: xVal4,
          y: yVal4,
        });
        xVal4++;
      }

      chart4.render();
    };

      var xVal5 = 0;
      var yVal5 = 0;
      var updateChart5 = function (count) {
        count = count || 1;

        for (var j = 0; j < count; j++) {
          yVal5 = parseFloat(json_data["pid_signal"]);
          dps5.push({
            x: xVal5,
            y: yVal5,
          });
          xVal5++;
        }

        chart5.render();
      };

    updateChart1(dataLength);
    updateChart2(dataLength);
    updateChart3(dataLength);
    updateChart4(dataLength);
    updateChart5(dataLength);
    setInterval(updateChart1, updateInterval);
    setInterval(updateChart2, updateInterval);
    setInterval(updateChart3, updateInterval);
    setInterval(updateChart4, updateInterval);
    setInterval(updateChart5, updateInterval);
  };