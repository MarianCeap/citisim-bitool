
function launchNSModal(){

      $('#nsAddBtn')[0].setAttribute("style","")
      $('#nsSaveBtn')[0].setAttribute("style","display:none;")
      $('.ui.basic.modal.NS').modal('show');
}

function nsModalCancel(){
    $('#nsName')[0].value = "";
    $('#nsValue')[0].value = "";
    $('#nsDuration')[0].value = "";
    $('#nsDescription')[0].value = "";
}

function nsModalAdd(){
    var name = $('#nsName')[0].value;
    var value = $('#nsValue')[0].value;
    var valueType = $('#nsValueType').html();
    var duration = $('#nsDuration')[0].value;
    var durationType = $('#nsDurationType').html();
    var description = $('#nsDescription')[0].value;

    if(name == "" || value == "" || duration == ""){
      alert("One of the required fields is empty!!!");
    }
    var request = $.ajax({
      type: "post",
      url: "/citisim/newScenario",
      contentType: "application/json",
      data: JSON.stringify({ "name": name,
                             "value": value,
                             "valueType" : valueType,
                             "duration": duration,
                             "durationType": durationType,
                             "description": description
                           }),

    });

    request.fail(function(jqXHR,textStatus,errorThrown){
      alert("The following error occurred: " + errorThrown);
    });

    request.done(function(response, textStatus, jqXHR){
      if(response.substring(0,5) == "rowid"){
        addNewScenario(name, value, valueType, duration, durationType, description, response.substring(6));
      }
    });

}

function addNewScenario(name, value, valueType, duration, durationType, description, scenarioID){
    var htmlStr = "<div id='scenario_"+scenarioID+"'>" +
              "<i  class='close icon pointed'  data-content='Remove Scenario' onclick='launchRMVSModal("+scenarioID+");'></i>" +
              "<i  class='edit icon pointed'  data-content='Edit Scenario' onclick='launchNSModalToEdit("+scenarioID+");'></i>" +
              "<div class='ui segment' style='color:black'>" +
                  "<div class='ui two column very relaxed divided grid'>" +
                      "<div id='details_"+ scenarioID +"' class='pointed column' style='width:30%' onclick='enterScenario("+scenarioID+")'>" +
                          "<h4 ><strong>" + name + "</strong></h4>" +
                          "Value: " + value + " " + valueType + "<br>" +
                          "Duration: " + duration + " " + durationType + "<br>" +
                          description +
                      "</div>" +
                      "<div class='column' style='width:70%'>" +
                          "<div class='ui grid'>" +
                              "<div id='rulesCol_" + scenarioID + "' class='fourteen wide column' style='padding-left:0; padding-right:0;'>" +
                                  "<h4><strong>Rules</strong></h4>" +
                              "</div>" +
                              "<div class='two wide column' align='right' style='padding-left:0'>" +
                                  "<i  id='addRuleButton' class='plus icon' data-content='Add New Rule' onclick='launchRLSModal("+scenarioID+")'></i>" +
                              "</div>" +
                          "</div>" +
                      "</div>" +
                  "</div>" +
              "</div>" +
              "<br>" +
          "</div>"

      $("#scenariosSegment").append(htmlStr);
      $('i').popup({on: 'hover'});
}

function getScenarios(){
  var request = $.ajax({
                          type: "get",
                          url: "/getScenarios",
                      });

  request.fail(function(jqXHR,textStatus,errorThrown){
    alert("The following error occurred: " + errorThrown);
  });

  request.done(function(response, textStatus, jqXHR){
    var resultSet = JSON.parse(response);

    for (var key in resultSet){
      var row = resultSet[key];
      addNewScenario(row['Name'],
                     row['Value'],
                     row['ValueType'],
                     row['Duration'],
                     row['DurationType'],
                     row['Description'],
                     row['ID']);

    }

  });
}

function launchRMVSModal(id){
    $('#rmvID')[0].value = id;
    $('.ui.basic.modal.RMVS').modal('show');
}

function rmvModalYes(){
    var id = $('#rmvID')[0].value;

    var request = $.ajax({
      type: "post",
      url: "/citisim/removeScenario",
      contentType: "application/json",
      data: JSON.stringify({ "id": id  })
    });


    request.fail(function(jqXHR,textStatus,errorThrown){
      alert("The following error occurred: " + errorThrown);
    });

    request.done(function(response, textStatus, jqXHR){
      var element = $('#scenario_' + id)[0];
      element.remove();
    });

}


function launchNSModalToEdit(id){
  var request = $.ajax({
      type: "post",
      url: "/citisim/getOneScenario",
      contentType: "application/json",
      data: JSON.stringify({ "id": id  })
    });


    request.fail(function(jqXHR,textStatus,errorThrown){
      alert("The following error occurred: " + errorThrown);
    });

    request.done(function(response, textStatus, jqXHR){
        var resultSet = JSON.parse(response);
        var row = resultSet[id];

        $('#nsID')[0].value = id;
        $('#nsName')[0].value = row['Name'];
        $('#nsValue')[0].value = row['Value'];
        $('#nsValueType').html(row['ValueType']);
        $('#nsDuration')[0].value = row['Duration'];
        $('#nsDurationType').html(row['DurationType']);
        $('#nsDescription')[0].value = row['Description'];

        $('#nsAddBtn')[0].setAttribute("style","display:none;")
        $('#nsSaveBtn')[0].setAttribute("style","")
        $('.ui.basic.modal.NS').modal('show');
    });

}



function nsModalSave(){
    var id = $('#nsID')[0].value;
    var name = $('#nsName')[0].value;
    var value = $('#nsValue')[0].value;
    var valueType = $('#nsValueType').html();
    var duration = $('#nsDuration')[0].value;
    var durationType = $('#nsDurationType').html();
    var description = $('#nsDescription')[0].value;

    if(name == "" || value == "" || duration == ""){
      alert("One of the required fields is empty!!!");
      return;
    }

    var request = $.ajax({
      type: "post",
      url: "/citisim/updateScenario",
      contentType: "application/json",
      data: JSON.stringify({ "id": id,
                             "name": name,
                             "value": value,
                             "valueType" : valueType,
                             "duration": duration,
                             "durationType": durationType,
                             "description": description
                           }),

    });

    request.fail(function(jqXHR,textStatus,errorThrown){
      alert("The following error occurred: " + errorThrown);
    });

    request.done(function(response, textStatus, jqXHR){
      $('#details_' + id).html("<h4 ><strong>" + name + "</strong></h4>" +
                               "Value: " + value + " " + valueType + "<br>" +
                               "Duration: " + duration + " " + durationType + "<br>" +
                               description);
    });
}


function enterScenario(id){
    window.location.href = "/citisim/biPage?scenarioID=" + id;

}

function launchComparePage(){
    window.location.href = "/citisim/comparePage"
}
