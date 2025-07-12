// 악기 목록
const instruments = ["vocals", "drums", "bass", "piano", "other"];

const sliderContainer = document.getElementById("sliders-container");

instruments.forEach(inst => {
  // 슬라이더 그룹 div
  const group = document.createElement("div");
  group.style.marginBottom = "16px";

  // 라벨
  const label = document.createElement("label");
  label.innerText = `${inst} volume (dB): `;

  // 값 표시
  const valueDisplay = document.createElement("span");
  valueDisplay.id = `${inst}-value`;
  valueDisplay.innerText = "0";

  // 슬라이더
  const slider = document.createElement("input");
  slider.type = "range";
  slider.min = -36;
  slider.max = 36;
  slider.value = 0;
  slider.step = 1;
  slider.id = `${inst}-slider`;
  slider.oninput = () => {
    document.getElementById(`${inst}-value`).innerText = slider.value;
  };

  // 그룹에 추가
  group.appendChild(label);
  group.appendChild(slider);
  group.appendChild(valueDisplay);

  sliderContainer.appendChild(group);
});

// 믹싱 버튼 클릭 이벤트
function applyMix() {
  const settings = {};
  instruments.forEach(inst => {
    const value = document.getElementById(`${inst}-slider`).value;
    settings[inst] = parseInt(value);
  });

  console.log("🎚️ 적용된 볼륨 설정:", settings);

  // 여기에 서버로 전송하거나 처리하는 코드 추가 가능
  alert("믹싱 설정이 콘솔에 출력되었습니다. 서버 연동은 별도 구현 필요.");
}
