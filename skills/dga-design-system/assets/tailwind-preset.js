// GENERATED FROM tokens.json — DO NOT EDIT BY HAND.
// Source: https://design.dga.gov.sa/ | Retrieved: 2026-08-26
// Regenerate: node generate-tokens.mjs
//
// Breakpoints follow DGA: Mobile 0-599 | Tablet 600-959 | Desktop 960-1279 | XL 1280+
// Use LOGICAL utilities only (ms-/me-/ps-/pe-/start-/end-), never ml-/mr-/left-/right-.
export default {
  theme: {
    screens: { sm: '600px', md: '960px', lg: '1280px' },
    extend: {
      colors: {
          "primary-sa-flag": {
                "25": "#f7fdf9",
                "50": "#f3fcf6",
                "100": "#dff6e7",
                "200": "#b8eacb",
                "300": "#88d8ad",
                "400": "#54c08a",
                "500": "#25935f",
                "700": "#166a45",
                "800": "#14573a",
                "900": "#104631",
                "950": "#092a1e"
          },
          "brand": {
                "25": "#f7fdf9",
                "50": "#f3fcf6",
                "100": "#dff6e7",
                "200": "#b8eacb",
                "300": "#88d8ad",
                "400": "#54c08a",
                "500": "#25935f",
                "600": "#1b8354",
                "700": "#166a45",
                "800": "#14573a",
                "900": "#104631",
                "950": "#092a1e"
          },
          "secondary-gold": {
                "25": "#fffef7",
                "50": "#fffef2",
                "100": "#fffce6",
                "200": "#fcf3bd",
                "300": "#fae996",
                "400": "#f7d54d",
                "500": "#f5bd02",
                "700": "#b87b02",
                "800": "#945c01",
                "900": "#6e3c00",
                "950": "#472400"
          },
          "tertiary-lavendar": {
                "25": "#fefcff",
                "50": "#f9f5fa",
                "100": "#f2e9f5",
                "200": "#e1cce8",
                "300": "#ccadd9",
                "400": "#a57bba",
                "600": "#6d428f",
                "700": "#532d75",
                "800": "#3d1d5e",
                "900": "#281047",
                "950": "#16072e"
          },
          "neutral": {
                "25": "#fcfcfd",
                "50": "#f9fafb",
                "100": "#f3f4f6",
                "200": "#e5e7eb",
                "300": "#d2d6db",
                "400": "#9da4ae",
                "500": "#6c727e",
                "600": "#4d5761",
                "700": "#384250",
                "800": "#1f2a37",
                "900": "#111927",
                "950": "#0c111b"
          },
          "gray": {
                "25": "#fafafa",
                "50": "#f5f5f6",
                "100": "#f0f1f1",
                "200": "#ececed",
                "300": "#cecfd2",
                "400": "#94969c",
                "500": "#85888e",
                "600": "#61646c",
                "700": "#333741",
                "800": "#1f242f",
                "900": "#161b26",
                "950": "#0c111d",
                "1000": "#161616"
          },
          "error": {
                "25": "#fffbfa",
                "50": "#fef3f2",
                "100": "#fee4e2",
                "200": "#fecdca",
                "300": "#fda29b",
                "400": "#f97066",
                "500": "#f04438",
                "600": "#d92d20",
                "700": "#b42318",
                "800": "#912018",
                "900": "#7a271a",
                "950": "#55160c"
          },
          "warning": {
                "25": "#fffcf5",
                "50": "#fffaeb",
                "100": "#fef0c7",
                "200": "#fedf89",
                "300": "#fec84b",
                "400": "#fdb022",
                "500": "#f79009",
                "600": "#dc6803",
                "700": "#b54708",
                "800": "#93370d",
                "900": "#7a2e0e",
                "950": "#4e1d09"
          },
          "success": {
                "25": "#f6fef9",
                "50": "#ecfdf3",
                "100": "#dcfae6",
                "200": "#abefc6",
                "300": "#75e0a7",
                "400": "#47cd89",
                "500": "#17b26a",
                "600": "#079455",
                "700": "#067647",
                "800": "#085d3a",
                "900": "#074d31",
                "950": "#053321"
          },
          "info": {
                "25": "#f5faff",
                "50": "#eff8ff",
                "100": "#d1e9ff",
                "200": "#b2ddff",
                "300": "#84caff",
                "400": "#53b1fd",
                "500": "#2e90fa",
                "600": "#1570ef",
                "700": "#175cd3",
                "800": "#1849a9",
                "900": "#194185",
                "950": "#102a56"
          },
          "base": {
                "white": "#ffffff",
                "black": "#161616"
          },
          "text": {
                "default": "#161616",
                "display": "#1f2a37",
                "primary-paragraph": "#384250",
                "secondary-paragraph": "#6c727e",
                "primary": "#1b8354",
                "secondary": "#dba102",
                "tertiary": "#80519f",
                "primary-sa-flag": "#14573a",
                "success": "#067647",
                "info": "#175cd3",
                "warning": "#b54707",
                "error": "#b42318",
                "primary-light": "#88d8ad",
                "secondary-light": "#fae996",
                "tertiary-light": "#ccadd9",
                "oncolor-primary": "#ffffff",
                "oncolor-secondary": "#ffffffcc",
                "oncolor-tertiary": "#ffffffb2",
                "default-disabled": "#9da4ae",
                "default-oncolor-disabled": "#ffffff66"
          },
          "background": {
                "white": "#ffffff",
                "body": "#f9fafb",
                "menu": "#ffffff",
                "card": "#ffffff",
                "black": "#161616",
                "surface-oncolor": "#ffffff",
                "brand-light": "#f3fcf6",
                "neutral-25": "#fcfcfd",
                "neutral-50": "#f9fafb",
                "neutral-100": "#f3f4f6",
                "neutral-200": "#e5e7eb",
                "neutral-300": "#d2d6db",
                "neutral-400": "#9da4ae",
                "neutral-800": "#1f2a37",
                "primary": "#1b8354",
                "primary-25": "#f7fdf9",
                "primary-50": "#f3fcf6",
                "primary-200": "#b8eacb",
                "primary-400": "#54c08a",
                "secondary": "#dba102",
                "secondary-25": "#fffef7",
                "secondary-50": "#fffef2",
                "tertiary": "#6d428f",
                "tertiary-25": "#fefcff",
                "tertiary-50": "#f9f5fa",
                "success": "#069454",
                "success-light": "#ecfdf3",
                "success-25": "#f6fef9",
                "success-50": "#ecfdf3",
                "info": "#156fee",
                "info-light": "#eff8ff",
                "info-25": "#f5faff",
                "info-50": "#eff8ff",
                "warning": "#dc6803",
                "warning-light": "#fffaeb",
                "warning-25": "#fffcf5",
                "warning-50": "#fffaeb",
                "error": "#d92c20",
                "error-light": "#fef3f2",
                "error-25": "#fffbfa",
                "error-50": "#fef3f2",
                "sa-flag": "#074c30",
                "sa-flag-25": "#f6fef9",
                "sa-flag-50": "#ecfdf3",
                "disabled": "#e5e7eb",
                "disabled-primary": "#b8eacb",
                "inverse-disabled": "#f3f4f6"
          }
    },
      spacing: {
          "0": "0px",
          "1": "4px",
          "2": "8px",
          "3": "12px",
          "4": "16px",
          "5": "20px",
          "6": "24px",
          "8": "32px",
          "10": "40px",
          "12": "48px",
          "16": "64px",
          "20": "80px",
          "24": "96px",
          "32": "128px",
          "40": "160px",
          "48": "192px",
          "56": "224px",
          "64": "256px",
          "80": "320px",
          "96": "384px",
          "120": "480px",
          "140": "560px",
          "160": "640px",
          "180": "720px",
          "192": "768px",
          "256": "1024px",
          "320": "1280px",
          "360": "1440px",
          "400": "1600px",
          "480": "1920px",
          "0.5": "2px",
          "1.5": "6px",
          "none": "0px",
          "xxs": "2px",
          "xs": "4px",
          "sm": "6px",
          "md": "8px",
          "lg": "12px",
          "xl": "16px"
    },
      borderRadius: {
          "none": "0",
          "xxs": "2px",
          "xs": "2px",
          "sm": "4px",
          "md": "8px",
          "lg": "16px",
          "xl": "24px",
          "2xl": "16px",
          "3xl": "20px",
          "4xl": "24px",
          "full": "9999px"
    },
      boxShadow: {
          "xs": "0px 1px 2px 0px rgba(16, 24, 40, .05)",
          "sm": "0px 1px 2px 0px rgba(16, 24, 40, .06), 0px 1px 3px 0px rgba(16, 24, 40, .1)",
          "md": "0px 2px 4px -2px rgba(16, 24, 40, .06), 0px 4px 8px -2px rgba(16, 24, 40, .1)",
          "lg": "0px 4px 6px -2px rgba(16, 24, 40, .03), 0px 12px 16px -4px rgba(16, 24, 40, .08)",
          "xl": "0px 8px 8px -4px rgba(16, 24, 40, .03), 0px 20px 24px -4px rgba(16, 24, 40, .08)",
          "2xl": "0px 24px 48px -12px rgba(16, 24, 40, .18)",
          "3xl": "0px 32px 64px -12px rgba(16, 24, 40, .14)"
    },
      fontSize: {
          "display-2xl": [
                "72px",
                {
                      "lineHeight": "90px",
                      "letterSpacing": "-0.02em"
                }
          ],
          "display-xl": [
                "60px",
                {
                      "lineHeight": "72px",
                      "letterSpacing": "-0.02em"
                }
          ],
          "display-lg": [
                "48px",
                {
                      "lineHeight": "60px",
                      "letterSpacing": "-0.02em"
                }
          ],
          "display-md": [
                "36px",
                {
                      "lineHeight": "44px",
                      "letterSpacing": "-0.02em"
                }
          ],
          "display-sm": [
                "30px",
                {
                      "lineHeight": "38px"
                }
          ],
          "display-xs": [
                "24px",
                {
                      "lineHeight": "32px"
                }
          ],
          "text-xl": [
                "20px",
                {
                      "lineHeight": "30px"
                }
          ],
          "text-lg": [
                "18px",
                {
                      "lineHeight": "28px"
                }
          ],
          "text-md": [
                "16px",
                {
                      "lineHeight": "24px"
                }
          ],
          "text-sm": [
                "14px",
                {
                      "lineHeight": "20px"
                }
          ],
          "text-xs": [
                "12px",
                {
                      "lineHeight": "18px"
                }
          ],
          "text-2xs": [
                "10px",
                {
                      "lineHeight": "14px"
                }
          ]
    },
      maxWidth: { paragraph: '720px', container: '1280px' },
      fontFamily: { sans: ['IBM Plex Sans', 'system-ui', 'sans-serif'] },
    },
  },
}
