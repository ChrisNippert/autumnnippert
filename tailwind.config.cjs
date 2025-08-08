/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/**/*.{astro,md,mdx,js,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0B0F14',
          soft: '#0F1520',
          card: '#121927'
        },
        text: {
          DEFAULT: '#E6ECF1',
          muted: '#B7C2CC'
        },
        accent: {
          DEFAULT: '#7C6FF4',
          soft: '#A3BFFA'
        },
        border: 'rgba(163,191,250,0.12)'
      }
    }
  },
  plugins: [require('@tailwindcss/typography')]
}
