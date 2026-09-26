import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        canvas: '#0A0A0A',
        'surface-1': '#121212',
        'surface-2': '#1E1E1E',
        'surface-3': '#2A2A2A',
        'surface-4': '#161616',
        'stroke': '#3F3F46',
        'saffron': '#FF671F',
        'saffron-dark': '#FF671F',
        'saffron-hover': '#E05A1B',
        'india-green': '#138808',
        'india-green-dark': '#046A38',
        'navy': '#002868',
        'accent-blue': '#3B82F6',
        'accent-blue-light': '#60A5FA',
        'text-primary': '#FFFFFF',
        'text-body': '#E5E7EB',
        'text-secondary': '#A1A1AA',
        'text-muted': '#71717A',
        'text-blue': '#60A5FA',
        'border-default': '#2A2A2A',
        'border-active': '#3F3F46',
      },
      fontFamily: {
        sans: ['"Roboto Flex"', '"Open Sans"', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'sm': '0.125rem',
        'DEFAULT': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
      },
      spacing: {
        'gutter': '1.5rem',
        'gutter-mobile': '1rem',
      },
    },
  },
  plugins: [],
};
export default config;
