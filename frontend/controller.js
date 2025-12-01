$(document).ready(function () {
  // Display Speak Message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    $("#SiriWave").attr("hidden", false);
    $(".siri-message").each(function () {
      var $el = $(this);
      // Stop any current animation
      try { $el.textillate('stop'); } catch (e) { /* ignore if not initialized yet */ }

      var $texts = $el.find('.texts');
      if ($texts.length) {
        $texts.html('<li>' + message + '</li>');
      } else {
        $el.html('<ul class="texts"><li>' + message + '</li></ul>');
      }

      // Start animation with the new text
      try { $el.textillate('start'); } catch (e) { /* if textillate not loaded, fallback to simple text */ $el.text(message); }
    });
  }
  eel.expose(ShowHood);
  function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
  }

  
  eel.expose(senderText);
  function senderText(message) {
    var chatBox = document.getElementById("chat-canvas-body");
    if (message.trim() !== "") {
      chatBox.innerHTML += `<div class="row justify-content-end mb-4">
          <div class = "width-size">
          <div class="sender_message">${message}</div>
      </div>`;

      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }

  eel.expose(receiverText);
  function receiverText(message) {
    var chatBox = document.getElementById("chat-canvas-body");
    if (message.trim() !== "") {
      chatBox.innerHTML += `<div class="row justify-content-start mb-4">
          <div class = "width-size">
          <div class="receiver_message">${message}</div>
          </div>
      </div>`;

      // Scroll to the bottom of the chat box
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  }
  
  eel.expose(hideLoader);
  function hideLoader() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
  }
  // Hide Face auth and display Face Auth success animation
  eel.expose(hideFaceAuth);
  function hideFaceAuth() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
  }
  // Hide success and display
  eel.expose(hideFaceAuthSuccess);
  function hideFaceAuthSuccess() {
    $("#FaceAuthSuccess").attr("hidden", true);
    $("#HelloGreet").attr("hidden", false);
  }

  // Hide Start Page and display blob
  eel.expose(hideStart);
  function hideStart() {
    $("#Start").attr("hidden", true);

    setTimeout(function () {
      $("#Oval").addClass("animate__animated animate__zoomIn");
    }, 1000);
    setTimeout(function () {
      $("#Oval").attr("hidden", false);
    }, 500);
  }
});