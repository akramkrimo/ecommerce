// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
const colors = require('tailwindcss/colors')

module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily:{
        'yeon-sung': ['Yeon Sung']
      },
      colors:{
        'blue-gray': colors.blueGray,
        'teal': colors.teal,
        'emerald': colors.emerald,
      }
  },
  variants: {
    extend: {},
  },
  plugins: [],
},
}
