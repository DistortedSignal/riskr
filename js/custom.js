function getStatus() {
  $.get("status/5").done(getStatusSuccess).fail(getStatusFail);
}

function getQueue() {
  $.get("queue").done(getQueueSuccess);
}

function generateQueueTableRow(queue_data) {
  //Refactor this and generateStatusTableRow into one function
  return"<tr><td>" + queue_data.name + "</td><td>" +
    queue_data.branch + "</td></tr>";
}

function getQueueSuccess(queueData) {
  var queue_arr = JSON.parse(queueData);
  $('#queue-table tbody').empty()

  for (var i = 0; i < queue_arr.length; i++) {
    if (i === 0) {
      $('#queue-table tbody').html(generateQueueTableRow(queue_arr[i]));
    } else {
      $('#queue-table tbody tr:last').after(generateQueueTableRow(queue_arr[i]));
    }
  }
}

function setBackgroundAndMessage(build_status, build_is_running) {
  var new_class = "build-";
  var status_message = "";
  
  if (build_is_running && $('body').attr('class').indexOf("static") > -1) {
    new_class = new_class + "working-";
  } else {
    new_class = new_class + "static-";
  }

  switch (build_status) {
    case "Complete":
      new_class = new_class + "success";
      status_message = "The previous build succeeded";
      break;
    case "Failed":
      new_class = new_class + "failed";
      status_message = "The previous build failed";
      break;
    case "Aborted":
    case "Aborting":
      new_class = new_class + "aborted";
      status_message = "The previous build was aborted";
      break;
    default:
      setStatusClass("server-error");
      $("#Content-p1").text("There was an error communicating with the server.");
      return;
  }

  if (build_is_running) {
    status_message = status_message + " and another build is running.";
  } else {
    status_message = status_message + ".";
  }

  $("#Content-p1").text(status_message);
  setStatusClass(new_class);
}

function generateStatusTableRow(build_status) {
  return "<tr><td>" + build_status.build_date + "</td><td>" +
    build_status.build_life_id + "</td><td>" + build_status.build_status + 
    "</td></tr>";
}

function getStatusSuccess(anthillStatusData) {
  // Python returns a string with single quotes; we have to change that to 
  // double quote
  anthillStatusData = anthillStatusData.replace(/'/g, '"');
  var status_arr = JSON.parse(anthillStatusData);
  var build_is_running = false;
  var previous_build_status = "";

  // Clear the table of previous runs
  $('#run-table tbody').empty();

  for (var i = 0; i < status_arr.length; i++) {
    //Set a row in a table... eventually
    if (i === 0) {
      $('#run-table tbody').html(generateStatusTableRow(status_arr[i]));
    } else {
      $('#run-table tbody tr:last').after(generateStatusTableRow(status_arr[i]));
    }

    //If the build is running, set up a breathing pattern.
    if (status_arr[i].build_status === "Running") {
      build_is_running = true;
    }

    if (previous_build_status === "" && status_arr[i].build_status !== "Running") {
      previous_build_status = status_arr[i].build_status;
    }
  }

  setBackgroundAndMessage(previous_build_status, build_is_running);
}

function getStatusFail() {
  setStatusClass("server-error");
  $("#Content-p1").text("There was an error communicating with the server.");
}

function setStatusClass(statusClass) {
  var classNameList = $('body').attr('class').split(/\s+/);

  for (var i = 0; i < classNameList.length; i++) {
    if (classNameList[i] === 'simple-transition') {
      continue;
    }
    $('body').removeClass(classNameList[i]);
  }

  $('body').addClass(statusClass);
}
