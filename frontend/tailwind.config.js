/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#24721b",
        danger: "#C0392B",
        success: "#1E8449",
      }
    },
  },
  plugins: [],
}