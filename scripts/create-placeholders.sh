#!/bin/bash
# Create SVG placeholder images for Kirameki Farm LP
# Uses warm brand colors: #fdfaf4 (cream), #8b6914 (gold), #231815 (dark brown)

IMAGES_DIR="/Users/simterm2026/Documents/claude/cc/kirameki-lp/public/images"

create_svg() {
    local filename="$1"
    local label="$2"
    local width="${3:-1200}"
    local height="${4:-800}"
    local bg1="${5:-#fdfaf4}"
    local bg2="${6:-#e8dcc8}"
    local accent="${7:-#8b6914}"

    cat > "${IMAGES_DIR}/${filename}" << EOF
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${bg1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:${bg2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#bg)" />
  <rect x="20" y="20" width="$((width-40))" height="$((height-40))" rx="8" fill="none" stroke="${accent}" stroke-width="2" stroke-dasharray="8,4" opacity="0.3" />
  <text x="50%" y="45%" text-anchor="middle" font-family="serif" font-size="36" fill="#231815" opacity="0.7">${label}</text>
  <text x="50%" y="55%" text-anchor="middle" font-family="sans-serif" font-size="16" fill="${accent}" opacity="0.5">Kirameki Farm — Placeholder Image</text>
</svg>
EOF
    echo "Created: ${filename}"
}

# Hero - wide format
create_svg "hero.svg" "Hero — Golden Hour Orchard" 1920 1080 "#fdfaf4" "#d4c4a0" "#8b6914"

# Concept section images
create_svg "knowledge.svg" "Knowledge — Farmer Inspecting Apple" 800 600 "#f5efe3" "#d9ccb0" "#6b5210"
create_svg "climate.svg" "Climate — Takayama Village Panorama" 1200 600 "#e8f0e8" "#c0d4c0" "#4a6b3a"
create_svg "soil.svg" "Soil — Rich Dark Earth" 800 600 "#d4c4a0" "#8b7040" "#3a2810"

# Philosophy
create_svg "philosophy.svg" "Philosophy — Farmer at Dawn" 1200 800 "#fdfaf4" "#e0d0b8" "#8b6914"

# Marquee images
create_svg "marquee-1.svg" "Marquee 1 — Red Apples" 600 400 "#f8e8e0" "#d4a090" "#8b3020"
create_svg "marquee-2.svg" "Marquee 2 — Shine Muscat" 600 400 "#e8f0e0" "#a0c890" "#4a6b30"
create_svg "marquee-3.svg" "Marquee 3 — Winter Pruning" 600 400 "#e8e8f0" "#b0b8d0" "#4a5070"
create_svg "marquee-4.svg" "Marquee 4 — Apple Blossoms" 600 400 "#fdf0f4" "#e0b0c0" "#8b4060"
create_svg "marquee-5.svg" "Marquee 5 — Harvested Apples" 600 400 "#f8e8d0" "#d4b890" "#8b6020"
create_svg "marquee-6.svg" "Marquee 6 — Sunset Vineyard" 600 400 "#f8e0c0" "#d4a060" "#8b5010"

# Product images
create_svg "shinano-sweet.svg" "Shinano Sweet Apple" 600 600 "#fdf0f0" "#e0b0a0" "#8b3020"
create_svg "shine-muscat.svg" "Shine Muscat Grapes" 600 600 "#f0f8f0" "#a0d0a0" "#3a6b30"
create_svg "sun-fuji.svg" "Sun Fuji Apple (Honey Core)" 600 600 "#fdf4e8" "#e0c090" "#8b5020"
create_svg "kyoho.svg" "Kyoho Grapes" 600 600 "#f0e8f4" "#b090c0" "#5a3070"

# Village aerial
create_svg "village.svg" "Village — Aerial View of Takayama" 1200 800 "#e8f0e8" "#c0d8b0" "#4a6b30"

echo ""
echo "All 16 placeholder SVG images created in ${IMAGES_DIR}/"
