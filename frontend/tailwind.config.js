/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'serif': ['mulish'],
      },
      colors: {
        'footer': '#013359',
        'footerGrey': '#333333',
        'plum': '#8C348A',
        'midnight' : '#003359'
      }
    },
  },
  plugins: [],
}