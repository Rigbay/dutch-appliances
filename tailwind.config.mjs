/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: '#1f2933',
        muted: '#627084',
        linen: '#f7f3ed',
        paper: '#fffdfa',
        leaf: '#28635b',
        clay: '#b7633f',
        brass: '#b4872c'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Fraunces', 'ui-serif', 'Georgia', 'serif']
      },
      boxShadow: {
        soft: '0 20px 50px rgba(31, 41, 51, 0.08)'
      }
    }
  },
  plugins: []
};
