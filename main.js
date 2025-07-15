// 실제 Render URL로 꼭 변경하세요!
const API_URL = "https://two025yjproject.onrender.com";

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
        // 캐시 문제 방지를 위해 타임스탬프 붙임
        document.getElementById("player").src = data.url + "?t=" + Date.now();
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById("status").innerText = "❌ 서버와 연결 실패";
    });
}
