// 👉 Render의 실제 URL로 변경해야 함
const API_URL = "https://your-render-app.onrender.com/api/mix";

function sendMix() {
  const settings = {
    voice: parseInt(document.getElementById("voice").value),
    drums: parseInt(document.getElementById("drums").value),
    bass: parseInt(document.getElementById("bass").value),
    other: parseInt(document.getElementById("other").value)
  };

  fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(settings)
  })
    .then(res => res.json())
    .then(data => {
      if (data.status === "error") {
        document.getElementById("status").innerText = "❌ 오류: " + data.message;
      } else {
        document.getElementById("status").innerText = "✅ 믹싱 완료!";
        document.getElementById("player").src = data.url + "?t=" + Date.now();
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById("status").innerText = "❌ 서버와 연결 실패";
    });
}
