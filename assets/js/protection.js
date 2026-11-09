/**
 * sIA Journal & Media Hub — Client-Side Shield & Content Protection
 * Canonical Author: cacs | https://escucha-sia.github.io
 */

(function () {
    'use strict';

    // 1. Bloquear Menú Contextual (Clic Derecho)
    document.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        return false;
    }, { capture: true });

    // 2. Bloquear Selección y Arrastre de Elementos
    document.addEventListener('selectstart', function (e) {
        // Permitir interacción solo con inputs si existieran
        if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            return false;
        }
    }, { capture: true });

    document.addEventListener('dragstart', function (e) {
        e.preventDefault();
        return false;
    }, { capture: true });

    // 3. Interceptar Atajos de Teclado Críticos (DevTools, Guardar, Imprimir, Copiar)
    document.addEventListener('keydown', function (e) {
        const key = e.key ? e.key.toLowerCase() : '';
        const isCtrl = e.ctrlKey || e.metaKey;

        // F12 (DevTools)
        if (e.key === 'F12' || e.keyCode === 123) {
            e.preventDefault();
            e.stopPropagation();
            return false;
        }

        // Atajos con Ctrl / Cmd
        if (isCtrl) {
            // Ctrl+C (Copiar), Ctrl+X (Cortar), Ctrl+A (Seleccionar todo)
            // Ctrl+U (Ver código fuente), Ctrl+S (Guardar página), Ctrl+P (Imprimir)
            if (['c', 'x', 'a', 'u', 's', 'p'].includes(key)) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }

            // Ctrl+Shift+I / Ctrl+Shift+J / Ctrl+Shift+C (DevTools Inspect)
            if (e.shiftKey && ['i', 'j', 'c'].includes(key)) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }
    }, { capture: true });

    // 4. Inyección de Atribución si se Forzara Alguna Copia
    document.addEventListener('copy', function (e) {
        e.preventDefault();
        if (e.clipboardData) {
            e.clipboardData.setData('text/plain', 'Contenido protegido por derechos de autor — sIA Journal (por cacs). Visita: https://escucha-sia.github.io');
        }
    }, { capture: true });

    // 5. Anti-Print: Escuchar evento beforeprint para ofuscar
    window.addEventListener('beforeprint', function () {
        document.body.style.display = 'none';
    });

    window.addEventListener('afterprint', function () {
        document.body.style.display = 'block';
    });

})();
