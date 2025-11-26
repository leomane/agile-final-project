const wheels = [
  document.querySelector('#wheel-1 .wheel-value'),
  document.querySelector('#wheel-2 .wheel-value'),
];
const wheelContainers = [
  document.querySelector('#wheel-1'),
  document.querySelector('#wheel-2'),
];
const wheelHandles = [
  document.querySelector('#wheel-1 .wheel-handle'),
  document.querySelector('#wheel-2 .wheel-handle'),
];
const spinButton = document.querySelector('#spin');
const statusEl = document.querySelector('#status');
const openaiStatusEl = document.querySelector('#openai-status');
const speciesNameEl = document.querySelector('#species-name');
const pairingEl = document.querySelector('#pairing');
const posterEl = document.querySelector('#poster');

console.log('[SpliceSafari] Booting UI script...');
console.log('[SpliceSafari] DOM hooks:', {
  wheels,
  wheelContainers,
  spinButton,
  wheelHandles,
  statusEl,
  openaiStatusEl,
  speciesNameEl,
  pairingEl,
  posterEl,
});

const fallbackAnimals = [
  'Lion',
  'Elephant',
  'Penguin',
  'Kangaroo',
  'Giraffe',
  'Panda',
  'Koala',
  'Falcon',
  'Octopus',
  'Dolphin',
  'Crocodile',
  'Armadillo',
  'Rabbit',
  'Hedgehog',
  'Otter',
  'Zebra',
  'Hippo',
  'Parrot',
  'Cheetah',
  'Meerkat',
  'Chameleon',
  'Wolf',
  'Fennec Fox',
  'Capybara',
  'Moose',
];

let spinIntervals = [];

function startWheelSpin() {
  console.log('[SpliceSafari] Starting wheel spin');
  wheelContainers.forEach((wheel) => wheel.classList.add('spin'));
  spinIntervals = wheelContainers.map((_, index) => {
    return setInterval(() => {
      const randomAnimal =
        fallbackAnimals[Math.floor(Math.random() * fallbackAnimals.length)];
      wheels[index].textContent = randomAnimal;
      if (index === 0 && Math.random() < 0.05) {
        console.log('[SpliceSafari] Wheel tick sample:', randomAnimal);
      }
    }, 90 + index * 10);
  });
}

function stopWheelSpin(finalAnimals) {
  console.log('[SpliceSafari] Stopping wheel spin. Final animals:', finalAnimals);
  wheelContainers.forEach((wheel) => wheel.classList.remove('spin'));
  spinIntervals.forEach(clearInterval);
  spinIntervals = [];
  finalAnimals.forEach((animal, index) => {
    wheels[index].textContent = animal;
  });
}

async function spinRoulette() {
  console.log('[SpliceSafari] Spin requested');
  spinButton.disabled = true;
  statusEl.textContent = 'Spinning both wheels and painting with AI...';
  startWheelSpin();

  try {
    console.log('[SpliceSafari] POST /api/spin');
    const response = await fetch('/api/spin', {
      method: 'POST',
    });
    console.log('[SpliceSafari] /api/spin response status:', response.status);
    if (!response.ok) {
      throw new Error('Failed to reach the animal lab');
    }
    const payload = await response.json();
    console.log('[SpliceSafari] /api/spin payload:', payload);

    stopWheelSpin(payload.animals);
    speciesNameEl.textContent = payload.speciesName;
    pairingEl.textContent = `${payload.animals[0]} + ${payload.animals[1]} = instant chaos.`;
    const imageData = payload.imageData || '';
    console.log('[SpliceSafari] image source tag:', payload.imageSource);
    console.log('[SpliceSafari] image data length:', imageData?.length || 0);
    posterEl.src = imageData || '/static/placeholder.svg';
    const sourceLabel =
      payload.imageSource === 'ai' && payload.imageData
        ? 'AI image generated'
        : 'Fallback illustration (API unavailable)';
    statusEl.textContent = `Generation complete — ${sourceLabel}.`;
  } catch (error) {
    console.error('[SpliceSafari] Spin failed:', error);
    stopWheelSpin([
      'Network gremlin',
      'Found',
    ]);
    statusEl.textContent = error.message;
  } finally {
    console.log('[SpliceSafari] Spin complete (success or error). Re-enabling button.');
    spinButton.disabled = false;
  }
}

spinButton.addEventListener('click', spinRoulette);
wheelHandles.forEach((handle) => {
  if (!handle) return;
  handle.addEventListener('click', (event) => {
    event.preventDefault();
    console.log('[SpliceSafari] Wheel handle clicked; starting unified spin');
    spinRoulette();
  });
});

async function loadOpenAIStatus() {
  console.log('[SpliceSafari] Loading OpenAI status pill');
  if (!openaiStatusEl) return;
  try {
    console.log('[SpliceSafari] GET /api/config');
    const response = await fetch('/api/config');
    console.log('[SpliceSafari] /api/config response status:', response.status);
    if (!response.ok) throw new Error('Unable to read painter status');
    const config = await response.json();
    console.log('[SpliceSafari] /api/config payload:', config);
    const reason = config.reason ? ` (${config.reason})` : '';
    if (config.openaiConfigured) {
      openaiStatusEl.textContent = `AI painter ready (${config.model})`;
      openaiStatusEl.classList.add('status-on');
      openaiStatusEl.classList.remove('status-off');
    } else {
      openaiStatusEl.textContent = `AI painter unavailable — using illustrated posters${reason}`;
      openaiStatusEl.classList.add('status-off');
      openaiStatusEl.classList.remove('status-on');
    }
  } catch (error) {
    console.error('[SpliceSafari] Failed to load painter status:', error);
    openaiStatusEl.textContent = 'Unable to reach painter status — using illustrated posters';
    openaiStatusEl.classList.add('status-off');
    openaiStatusEl.classList.remove('status-on');
  }
}

loadOpenAIStatus();
console.log('[SpliceSafari] UI script loaded');
