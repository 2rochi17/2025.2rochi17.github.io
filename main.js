const instruments = ["vocals", "drums", "bass", "piano", "other"];
const slidersContainer = document.getElementById("sliders-container");

const sliders = {};

instruments.forEach(inst => {
  const wrapper = document.createElement("div");
  wrapper.style.marginBottom = "10px";

  const label = document.createElement("label");
  label.innerText = `${inst} volume (dB): `;

  const value = document.createElement("span");
  value.id = `${inst}-val`;
  value.innerText = "0";

  const slider = document.createElement("input");
  slider.type = "range";
  slider.min = -36;
  slider.max = 36;
  slider.value = 0;
  slider.step = 1;
  slider.oninput = () => {
    value.innerText = slider.value;
  };

  sliders[inst] = slider;

  wrapper.appendChild(label);
  wrapper.appendChild(slider);
  wrapper.appendChild(value);

  slidersContainer.appendChild(wrapper);
});

function applyMix() {
  const values = {};
  instruments.forEach(inst => {
    values[inst] = parseInt(sliders[inst].value);
  });

  document.getElementById("status").innerText = "⏳ 믹싱 중...";
  fetch("/api/mix", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(values)
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("status").innerText = "✅ 믹싱 완료!";
      document.getElementById("player").src = data.url + "?t=" + Date.now(); // 캐시 방지
    })
    .catch(err => {
      console.error(err);
      document.getElementById("status").innerText = "❌ 에러 발생";
    });
}
