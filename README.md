<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Mini Ninja CSS</title>
    <style>
        :root {
            --ninja-red: #d32f2f;
            --ninja-black: #1a1a1a;
            --ninja-skin: #ffe0b2;
        }

        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }

        .ninja {
            position: relative;
            width: 100px;
            height: 150px;
        }

        /* Cabeça e Capuz */
        .head {
            position: absolute;
            width: 80px;
            height: 70px;
            background-color: var(--ninja-red);
            border-radius: 15px;
            left: 10px;
            z-index: 2;
        }

        /* Abertura da Máscara (Rosto) */
        .face-slot {
            position: absolute;
            width: 60px;
            height: 20px;
            background-color: var(--ninja-skin);
            top: 20px;
            left: 10px;
            border-radius: 5px;
            overflow: hidden;
        }

        /* Olhos */
        .eyes {
            position: absolute;
            width: 8px;
            height: 8px;
            background-color: black;
            border-radius: 50%;
            top: 6px;
            box-shadow: 35px 0 0 black; /* Segundo olho */
            left: 10px;
        }

        /* Corpo (Tronco) */
        .body {
            position: absolute;
            width: 90px;
            height: 80px;
            background-color: var(--ninja-red);
            top: 75px;
            left: 5px;
            border-radius: 10px 10px 5px 5px;
            border-bottom: 10px solid var(--ninja-black); /* Cinto */
        }

        /* Detalhe da roupa (O "V") */
        .detail {
            position: absolute;
            width: 0;
            height: 0;
            border-left: 20px solid transparent;
            border-right: 20px solid transparent;
            border-top: 40px solid var(--ninja-black);
            left: 25px;
            opacity: 0.3;
        }
    </style>
</head>
<body>

    <div class="ninja">
        <div class="head">
            <div class="face-slot">
                <div class="eyes"></div>
            </div>
        </div>
        <div class="body">
            <div class="detail"></div>
        </div>
    </div>

</body>
</html>