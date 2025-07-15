// ✅ Render에서 실제 URL로 교체 (이 부분만 바꾸면 끝!)
const API_URL = "https://audio-mix-render.onrender.com/api/mix";

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
        document.getElementById("player").src = data.url + "?t=" + Date.now(); // 캐싱 방지
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById("status").innerText = "❌ 서버와 연결 실패";
    });
}
