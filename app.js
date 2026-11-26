const state = { destinations: [], selectedDestination: null, selectedPackage: null, selectedHotel: null, slide: 0 };
const slides = [
  { image: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1300&q=85', location: 'Dolomites, Italy' },
  { image: 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1300&q=85', location: 'Bali, Indonesia' },
  { image: 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=1300&q=85', location: 'The Algarve, Portugal' },
];
const $ = (selector) => document.querySelector(selector);
const toast = (message, error = false) => { const element = $('#toast'); element.textContent = message; element.className = `toast visible${error ? ' error' : ''}`; setTimeout(() => element.className = 'toast', 3500); };
const money = (value) => new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', maximumFractionDigits: 0 }).format(value);

async function fetchDestinations() {
  const response = await fetch('/api/destinations');
  state.destinations = await response.json();
  $('#destination-grid').innerHTML = state.destinations.map((destination) => `
    <article class="destination-card" data-destination="${destination.id}">
      <img src="${destination.image}" alt="${destination.name}, ${destination.country}" loading="lazy">
      <div class="destination-card-content"><span class="destination-tag">${destination.tag}</span><h3>${destination.name}</h3><div class="destination-meta"><span>★ ${destination.rating} · ${destination.reviews} reviews</span><button type="button">Book now ↗</button></div></div>
    </article>`).join('');
  document.querySelectorAll('.destination-card').forEach((card) => card.addEventListener('click', () => openBooking(card.dataset.destination)));
}

function updateSlide(direction) {
  state.slide = (state.slide + direction + slides.length) % slides.length;
  const slide = slides[state.slide]; $('#hero-image').style.opacity = '0';
  setTimeout(() => { $('#hero-image').src = slide.image; $('#slide-location').textContent = slide.location; $('#slide-count').textContent = `0${state.slide + 1} / 03`; $('#hero-image').style.opacity = '1'; }, 200);
}

async function openBooking(destinationId) {
  const response = await fetch(`/api/destinations/${destinationId}`); state.selectedDestination = await response.json();
  state.selectedPackage = null; state.selectedHotel = null; $('#booking-modal').hidden = false; renderPackageStep();
}
function renderPackageStep() {
  const destination = state.selectedDestination;
  $('#booking-step').innerHTML = `<div class="booking-header"><p class="eyebrow">${destination.country} · ${destination.tag}</p><h2>Make ${destination.name}<br><em>yours.</em></h2><p class="section-description">Start with a package. You can choose your stay next.</p></div><div class="booking-options">${destination.packages.map((item) => `<button class="option-card package-option" data-id="${item.id}"><div><span class="destination-tag">${item.duration}</span></div><div><h3>${item.name}</h3><p>${item.summary}</p></div><strong>${money(item.price)}</strong></button>`).join('')}</div><div class="booking-next"><button class="button button-dark" id="package-next" disabled>Choose a stay <span>→</span></button></div>`;
  document.querySelectorAll('.package-option').forEach((card) => card.addEventListener('click', () => { state.selectedPackage = destination.packages.find((item) => item.id === card.dataset.id); document.querySelectorAll('.package-option').forEach((item) => item.classList.remove('selected')); card.classList.add('selected'); $('#package-next').disabled = false; }));
  $('#package-next').addEventListener('click', renderHotelStep);
}
function renderHotelStep() {
  const destination = state.selectedDestination;
  $('#booking-step').innerHTML = `<div class="booking-header"><p class="eyebrow">Step 2 of 3 · ${destination.name}</p><h2>Stay somewhere<br><em>special.</em></h2></div><div class="booking-options">${destination.hotels.map((item) => `<button class="option-card hotel-option" data-id="${item.id}"><img src="${item.image}" alt="${item.name}"><div><h3>${item.name}</h3><p>${item.type} · ★ ${item.rating}</p><p>${item.amenities.join(' · ')}</p></div><strong>${money(item.price)}<small>/ night</small></strong></button>`).join('')}</div><div class="booking-next"><button class="button button-dark" id="hotel-next" disabled>Continue to details <span>→</span></button></div>`;
  document.querySelectorAll('.hotel-option').forEach((card) => card.addEventListener('click', () => { state.selectedHotel = destination.hotels.find((item) => item.id === card.dataset.id); document.querySelectorAll('.hotel-option').forEach((item) => item.classList.remove('selected')); card.classList.add('selected'); $('#hotel-next').disabled = false; }));
  $('#hotel-next').addEventListener('click', renderDetailsStep);
}
function renderDetailsStep() {
  $('#booking-step').innerHTML = `<div class="booking-header"><p class="eyebrow">Step 3 of 3 · Nearly there</p><h2>Let’s make it<br><em>official.</em></h2></div><form class="booking-form" id="booking-form"><label>Your name<input name="guest_name" required placeholder="Full name"></label><label>Email address<input type="email" name="email" required placeholder="you@example.com"></label><label>Preferred check-in<input type="date" name="check_in" required></label><label>Guests<input type="number" name="guests" min="1" max="12" value="2" required></label><div class="booking-summary"><strong>${state.selectedDestination.name} · ${state.selectedPackage.name}</strong><br>${state.selectedHotel.name} · Package from ${money(state.selectedPackage.price)} + stay from ${money(state.selectedHotel.price)}/night</div><button class="button button-dark" type="submit">Review payment <span>↗</span></button></form>`;
  $('#booking-form').addEventListener('submit', async (event) => { event.preventDefault(); const form = new FormData(event.target); const payload = Object.fromEntries(form); payload.destination_id = state.selectedDestination.id; payload.package_id = state.selectedPackage.id; payload.hotel_id = state.selectedHotel.id; payload.guests = Number(payload.guests); const response = await fetch('/api/bookings', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) }); const result = await response.json(); if (!response.ok) return toast(result.detail || 'Please check your details.', true); renderSuccess(result); });
}
function renderSuccess(result) { $('#booking-step').innerHTML = `<div class="success-state"><div class="success-icon">✓</div><p class="eyebrow" style="justify-content:center">Payment details next</p><h2>Your trip is<br><em>on the map.</em></h2><p>${result.message}<br>Your reference is <strong>${result.reference}</strong>.</p><button class="button button-dark" data-close-booking>Done <span>↗</span></button></div>`; document.querySelector('[data-close-booking]').addEventListener('click', closeBooking); }
function closeBooking() { $('#booking-modal').hidden = true; }

document.querySelectorAll('[data-open-login]').forEach((button) => button.addEventListener('click', () => $('#login-dialog').showModal()));
document.querySelectorAll('.role-switch button').forEach((button) => button.addEventListener('click', () => { document.querySelectorAll('.role-switch button').forEach((item) => item.classList.remove('active')); button.classList.add('active'); document.querySelector('[name="role"]').value = button.dataset.role; }));
const loginForm = $('#login-form');
if (loginForm) loginForm.addEventListener('submit', async (event) => { event.preventDefault(); const payload = Object.fromEntries(new FormData(event.target)); const response = await fetch('/api/login', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) }); const result = await response.json(); $('#login-dialog').close(); toast(result.message); });
const contactForm = $('#contact-form');
if (contactForm) contactForm.addEventListener('submit', async (event) => { event.preventDefault(); const response = await fetch('/api/contact', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(Object.fromEntries(new FormData(event.target))) }); const result = await response.json(); toast(result.message); event.target.reset(); });
const previousButton = $('.previous');
const nextButton = $('.next');
if (previousButton) previousButton.addEventListener('click', () => updateSlide(-1));
if (nextButton) nextButton.addEventListener('click', () => updateSlide(1));
const closeBookingButton = $('[data-close-booking]');
if (closeBookingButton) closeBookingButton.addEventListener('click', closeBooking);
fetchDestinations().catch(() => toast('Could not load destinations.', true));
