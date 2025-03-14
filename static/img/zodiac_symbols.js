/**
 * SVG-символы знаков зодиака для использования в проекте
 */

const ZodiacSymbols = {
    'aries': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M50 15 C 30 35, 30 65, 50 85 M50 15 C 70 35, 70 65, 50 85 M25 40 H 75" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'taurus': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <circle cx="50" cy="65" r="20" stroke="#8a2be2" stroke-width="4" fill="none"/>
        <path d="M30 35 C 30 15, 70 15, 70 35 C 70 45, 60 50, 50 50 M50 50 C 40 50, 30 45, 30 35" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'gemini': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M35 20 V 80 M65 20 V 80 M35 35 H 65 M35 65 H 65" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'cancer': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M30 40 C 20 40, 20 60, 30 60 C 40 60, 40 40, 30 40 M70 40 C 80 40, 80 60, 70 60 C 60 60, 60 40, 70 40 M30 50 H 70" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'leo': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <circle cx="35" cy="40" r="15" stroke="#8a2be2" stroke-width="4" fill="none"/>
        <path d="M50 40 C 60 25, 80 25, 80 45 C 80 65, 60 65, 50 55 M50 55 C 40 65, 20 65, 20 45" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'virgo': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M30 30 C 30 50, 40 60, 50 60 C 60 60, 70 50, 70 30 M50 60 V 75 M40 40 C 40 50, 60 50, 60 40" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'libra': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M25 65 H 75 M25 50 H 75 M35 35 C 35 25, 65 25, 65 35 C 65 45, 35 45, 35 35" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'scorpio': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M20 50 C 20 40, 35 40, 35 50 C 35 60, 50 60, 50 50 C 50 40, 65 40, 65 50 L 75 40 M75 40 L 85 50" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'sagittarius': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M25 75 L 75 25 M75 25 H 55 M75 25 V 45 M40 60 L 60 40" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'capricorn': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M30 70 C 30 50, 40 50, 50 50 C 60 50, 70 60, 70 40 C 70 30, 65 25, 60 25 M50 50 V 75" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'aquarius': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M25 40 C 35 30, 45 50, 55 40 C 65 30, 75 50, 85 40 M25 60 C 35 50, 45 70, 55 60 C 65 50, 75 70, 85 60" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`,
    
    'pisces': `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
        <circle cx="50" cy="50" r="45" fill="#8a2be2" fill-opacity="0.1"/>
        <path d="M30 25 C 30 45, 30 55, 30 75 M70 25 C 70 45, 70 55, 70 75 M30 50 H 70" stroke="#8a2be2" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>`
}; 