const container = document.querySelector('.container');
const seats = document.querySelectorAll('.row .seat:not(.occupied)');
const count = document.getElementById('count');
const total = document.getElementById('total');
const movieSelect = document.getElementById('movie');
const seat_choose = document.getElementById('seat_choose');
const d = {
  2: 'A18', 3: 'A17', 4: 'A16', 5: 'A15', 6: 'A14', 7: 'A13', 8: 'A12', 9: 'A11', 10: 'A10', 11: 'A9', 12: 'A8', 13: 'A7', 14: 'A6', 15: 'A5', 16: 'A4', 17: 'A3', 18: 'A2', 19: 'A1',
  24: 'B18', 25: 'B17', 26: 'B16', 27: 'B15', 28: 'B14', 29: 'B13', 30: 'B12', 31: 'B11', 32: 'B10', 33: 'B9', 34: 'B8', 35: 'B7', 36: 'B6', 37: 'B5', 38: 'B4', 39: 'B3', 40: 'B2', 41: 'B1',
  46: 'C18', 47: 'C17', 48: 'C16', 49: 'C15', 50: 'C14', 51: 'C13', 52: 'C12', 53: 'C11', 54: 'C10', 55: 'C9', 56: 'C8', 57: 'C7', 58: 'C6', 59: 'C5', 60: 'C4', 61: 'C3', 62: 'C2', 63: 'C1',
  68: 'D18', 69: 'D17', 70: 'D16', 71: 'D15', 72: 'D14', 73: 'D13', 74: 'D12', 75: 'D11', 76: 'D10', 77: 'D9', 78: 'D8', 79: 'D7', 80: 'D6', 81: 'D5', 82: 'D4', 83: 'D3', 84: 'D2', 85: 'D1',
  90: 'E18', 91: 'E17', 92: 'E16', 93: 'E15', 94: 'E14', 95: 'E13', 96: 'E12', 97: 'E11', 98: 'E10', 99: 'E9', 100: 'E8', 101: 'E7', 102: 'E6', 103: 'E5', 104: 'E4', 105: 'E3', 106: 'E2', 107: 'E1',
  110: 'F22', 111: 'F21', 112: 'F20', 113: 'F19', 114: 'F18', 115: 'F17', 116: 'F16', 117: 'F15', 118: 'F14', 119: 'F13', 120: 'F12', 121: 'F11', 122: 'F10', 123: 'F9', 124: 'F8', 125: 'F7', 126: 'F6', 127: 'F5',
  128: 'F4', 129: 'F3', 130: 'F2', 131: 'F1'
}
populateUI();

let ticketPrice = +movieSelect.value;

// Save selected movie index and price
function setMovieData(movieIndex, moviePrice) {
  localStorage.setItem('selectedMovieIndex', movieIndex);
  localStorage.setItem('selectedMoviePrice', moviePrice);
}

// Update total and count
function updateSelectedCount() {
  const selectedSeats = document.querySelectorAll('.row .seat.selected');

  const seatsIndex = [...selectedSeats].map(seat => [...seats].indexOf(seat));

  localStorage.setItem('selectedSeats', JSON.stringify(seatsIndex));

  const selectedSeatsCount = selectedSeats.length;

  count.innerText = selectedSeatsCount;
  total.innerText = selectedSeatsCount * ticketPrice;
  var a = Number(JSON.parse(localStorage.getItem('selectedSeats')));
  seat_choose.innerText = d[a];
  setMovieData(movieSelect.selectedIndex, movieSelect.value);
}

// Get data from localstorage and populate UI
function populateUI() {
  const selectedSeats = JSON.parse(localStorage.getItem('selectedSeats'));

  if (selectedSeats !== null && selectedSeats.length > 0) {
    seats.forEach((seat, index) => {
      if (selectedSeats.indexOf(index) > -1) {
        seat.classList.add('selected');
      }
    });
  }

  const selectedMovieIndex = localStorage.getItem('selectedMovieIndex');

  if (selectedMovieIndex !== null) {
    movieSelect.selectedIndex = selectedMovieIndex;
  }
}

// Movie select event
movieSelect.addEventListener('change', e => {
  ticketPrice = +e.target.value;
  setMovieData(e.target.selectedIndex, e.target.value);
  updateSelectedCount();
  refreshSeat()
});

// Seat click event
container.addEventListener('click', e => {
  var selectedSeats = document.querySelectorAll('.row .seat.selected');
  Array.from(document.querySelectorAll('.row .seat.selected')).forEach(function (el) {
    el.classList.remove('selected');
  });
  updateSelectedCount;
  if (
    e.target.classList.contains('seat') &&
    !e.target.classList.contains('occupied')
  ) {
    e.target.classList.toggle('selected');
    updateSelectedCount();
  }
});

// Initial count and total set
updateSelectedCount();

//