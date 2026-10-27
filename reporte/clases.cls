\LoadClass[11pt,a4paper]{article}
% --- Paquetes de Idioma y Tipografía ---
\usepackage[utf8]{inputenc}
\usepackage[spanish,es-tabla]{babel}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{xcolor}

% --- Tablas Avanzadas (Estilo clases.tex / pixhawk_2_4_8.tex) ---
\usepackage{tabularray}
\UseTblrLibrary{booktabs}
\usepackage{booktabs}
\usepackage{caption}
\usepackage{subcaption}

% --- Geometría e Hipervínculos ---
\usepackage[top=2.5cm, bottom=2.5cm, left=2cm, right=2cm]{geometry}
\usepackage{hyperref}

\definecolor{colorreferences}{RGB}{48,134,3}
\definecolor{mintedbackground}{rgb}{0.95,0.95,0.95}

\hypersetup{
    colorlinks=true,
    linkcolor=black,
    citecolor=colorreferences,
    urlcolor=blue
}

\graphicspath{{img/}{portada/}}  % Las imágenes se buscarán en la carpeta "img"