const wheels = [
  document.querySelector('#wheel-1 .wheel-value'),
  document.querySelector('#wheel-2 .wheel-value'),
];
const wheelContainers = [
  document.querySelector('#wheel-1'),
  document.querySelector('#wheel-2'),
];
const spinButton = document.querySelector('#spin');
const statusEl = document.querySelector('#status');
const speciesNameEl = document.querySelector('#species-name');
const pairingEl = document.querySelector('#pairing');
const posterEl = document.querySelector('#poster');

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
  wheelContainers.forEach((wheel) => wheel.classList.add('spin'));
  spinIntervals = wheelContainers.map((_, index) => {
    return setInterval(() => {
      const randomAnimal =
        fallbackAnimals[Math.floor(Math.random() * fallbackAnimals.length)];
      wheels[index].textContent = randomAnimal;
    }, 90 + index * 10);
  });
}

function stopWheelSpin(finalAnimals) {
  wheelContainers.forEach((wheel) => wheel.classList.remove('spin'));
  spinIntervals.forEach(clearInterval);
  spinIntervals = [];
  finalAnimals.forEach((animal, index) => {
    wheels[index].textContent = animal;
  });
}

async function spinRoulette() {
  spinButton.disabled = true;
    statusEl.textContent = 'Spinning both wheels and painting with AI...';
  startWheelSpin();

  try {
    const response = await fetch('/api/spin', {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to reach the animal lab');
    }
    const payload = await response.json();

    stopWheelSpin(payload.animals);
    speciesNameEl.textContent = payload.speciesName;
    pairingEl.textContent = `${payload.animals[0]} + ${payload.animals[1]} = instant chaos.`;
    posterEl.src = payload.imageData;
    const sourceLabel =
      payload.imageSource === 'ai'
        ? 'AI image generated'
        : 'Fallback illustration (API unavailable)';
    statusEl.textContent = `Generation complete — ${sourceLabel}.`;
  } catch (error) {
    stopWheelSpin([
      'Network gremlin',
      'Found',
    ]);
    statusEl.textContent = error.message;
  } finally {
    spinButton.disabled = false;
  }
}

spinButton.addEventListener('click', spinRoulette);
