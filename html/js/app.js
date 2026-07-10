/**
 * ============================================================================
 * PyPharma Manager · Sistema de Farmacia Interactivo · Grupo 07
 * Lógica en JavaScript Vanilla (Simulación del modelo OOP de Python)
 * ============================================================================
 */

// ============================================================================
// 1. MODELOS DE CLASES (Orientado a Objetos - Equivalente a medicamento.py y pedido.py)
// ============================================================================

/**
 * Clase que representa un Medicamento en el inventario de la farmacia.
 * Equivalente a `clases/medicamento.py`
 */
class Medicamento {
    constructor(stock, nombre, precio) {
        this.stock = parseInt(stock, 10);
        this.nombre = String(nombre);
        this.precio = parseFloat(precio);
    }

    /**
     * Aplica un porcentaje de descuento (0 a 100) sobre el precio actual.
     */
    aplicarDescuento(porcentaje) {
        const descuento = this.precio * (porcentaje / 100);
        this.precio -= descuento;
        return `Se aplicó ${porcentaje}% de descuento. Nuevo precio: $${this.precio.toFixed(2)}`;
    }

    /**
     * Disminuye el stock disponible al realizar una venta o pedido.
     */
    reducirStock(cantidad) {
        if (cantidad > this.stock) {
            throw new Error(`No hay suficiente stock de ${this.nombre} (Disponible: ${this.stock}).`);
        }
        this.stock -= cantidad;
        return `Stock actualizado. Quedan ${this.stock} unidades de ${this.nombre}.`;
    }

    /**
     * Convierte el objeto en un array estándar [stock, nombre, precio] para persistencia.
     */
    aLista() {
        return [this.stock, this.nombre, this.precio];
    }

    /**
     * Crea una instancia de Medicamento a partir de una lista o array [stock, nombre, precio].
     */
    static desdeLista(datos) {
        return new Medicamento(datos[0], datos[1], datos[2]);
    }
}

/**
 * Clase que representa un Pedido de compra realizado por un cliente en la farmacia.
 * Equivalente a `clases/pedido.py`
 */
class Pedido {
    constructor(cliente) {
        this.cliente = String(cliente);
        this.medicamentos = []; // Array de { medicamento: Medicamento, cantidad: Number }
    }

    /**
     * Agrega un medicamento al pedido y reduce su stock en el inventario.
     */
    agregarMedicamento(medicamento, cantidad) {
        medicamento.reducirStock(cantidad);
        this.medicamentos.push({
            medicamento: medicamento,
            cantidad: parseInt(cantidad, 10)
        });
    }

    /**
     * Calcula el costo total sumando el precio por cantidad de cada ítem en el carrito.
     */
    calcularTotal() {
        return this.medicamentos.reduce((total, item) => {
            return total + (item.medicamento.precio * item.cantidad);
        }, 0.0);
    }

    /**
     * Genera un array de filas [cliente, cantidad, nombre, precio, fecha] para el historial.
     */
    aFilasRegistro() {
        const fechaStr = new Date().toLocaleDateString('es-ES', { 
            day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' 
        });
        return this.medicamentos.map(item => [
            this.cliente,
            item.cantidad,
            item.medicamento.nombre,
            item.medicamento.precio,
            fechaStr
        ]);
    }
}


// ============================================================================
// 2. GESTIÓN DE PERSISTENCIA Y ESTADO GLOBAL (Simulación de gestion_archivos.py)
// ============================================================================

// Datos iniciales originales exactos del proyecto Python (inventario_medicinas.txt y registro_pedidos.txt)
const INVENTARIO_INICIAL = [
    [11, "Paracetamol", 0.3],
    [24, "Ibuprofeno", 0.85],
    [34, "Amoxicilina", 0.45],
    [13, "Losartan", 0.5],
    [10, "Omeprazol", 0.8],
    [34, "Aspirina", 0.9],
    [9,  "Tukol", 3.5],
    [7,  "Bismutol", 1.8],
    [17, "Cefalexina", 0.2],
    [30, "Loratadina", 0.25],
    [18, "Umbramil", 0.7]
];

const HISTORIAL_INICIAL = [
    ["Steven", 2, "Cefalexina", 0.2, "07/07/2026 10:15"],
    ["Steven", 1, "Paracetamol", 0.3, "07/07/2026 10:16"],
    ["Jonathan", 2, "Loratadina", 0.25, "07/07/2026 11:30"],
    ["Steven", 1, "Tukol", 3.5, "07/07/2026 14:20"]
];

// Estado de la Aplicación en Memoria
let inventario = [];
let historialPedidos = [];
let pedidoActual = null; // Instancia activa del carrito POS

/**
 * Carga los datos desde localStorage o inicializa con los datos del proyecto Python.
 */
function cargarDatos() {
    const invGuardado = localStorage.getItem('pypharma_inventario');
    const histGuardado = localStorage.getItem('pypharma_historial');

    if (invGuardado) {
        try {
            const arr = JSON.parse(invGuardado);
            inventario = arr.map(item => Medicamento.desdeLista(item));
        } catch (e) {
            inventario = INVENTARIO_INICIAL.map(item => Medicamento.desdeLista(item));
        }
    } else {
        inventario = INVENTARIO_INICIAL.map(item => Medicamento.desdeLista(item));
    }

    if (histGuardado) {
        try {
            historialPedidos = JSON.parse(histGuardado);
        } catch (e) {
            historialPedidos = [...HISTORIAL_INICIAL];
        }
    } else {
        historialPedidos = [...HISTORIAL_INICIAL];
    }
}

/**
 * Guarda el estado actual del inventario y del historial en localStorage.
 */
function guardarDatos() {
    const arrInv = inventario.map(med => med.aLista());
    localStorage.setItem('pypharma_inventario', JSON.stringify(arrInv));
    localStorage.setItem('pypharma_historial', JSON.stringify(historialPedidos));
    actualizarKPIs();
}

/**
 * Restablece los datos a los valores originales por defecto del archivo de texto.
 */
function restablecerDatosDemo() {
    if (confirm('¿Estás seguro de restablecer el inventario y las ventas a los datos originales de Python? Se perderán las modificaciones actuales.')) {
        localStorage.removeItem('pypharma_inventario');
        localStorage.removeItem('pypharma_historial');
        cargarDatos();
        actualizarKPIs();
        renderizarTodo();
        mostrarToast('Datos restablecidos exitosamente a los archivos originales.', 'success');
    }
}


// ============================================================================
// 3. FUNCIONES UTILITARIAS DE BÚSQUEDA (Equivalente a utilidades.py)
// ============================================================================

function buscarPorNombre(nombre) {
    const nombreLower = nombre.trim().toLowerCase();
    return inventario.find(m => m.nombre.toLowerCase() === nombreLower) || null;
}

function buscarCoincidencias(texto) {
    const query = texto.trim().toLowerCase();
    if (!query) return inventario;
    return inventario.filter(m => m.nombre.toLowerCase().includes(query));
}


// ============================================================================
// 4. ACTUALIZACIÓN DE INTERFAZ Y RENDERIZADO (DOM Manipulation)
// ============================================================================

/**
 * Actualiza las tarjetas estadísticas KPI de la parte superior.
 */
function actualizarKPIs() {
    const totalMed = inventario.length;
    const totalStock = inventario.reduce((sum, med) => sum + med.stock, 0);
    const valorInv = inventario.reduce((sum, med) => sum + (med.stock * med.precio), 0);
    const totalVentas = historialPedidos.length;

    document.getElementById('kpiTotalMed').textContent = totalMed;
    document.getElementById('kpiTotalStock').textContent = totalStock.toLocaleString();
    document.getElementById('kpiValorInv').textContent = `$${valorInv.toFixed(2)}`;
    document.getElementById('kpiTotalVentas').textContent = totalVentas;
}

/**
 * Renderiza la tabla general del Inventario en la pestaña 1.
 */
function renderizarTablaInventario(filtro = '') {
    const tbody = document.getElementById('tablaInventarioBody');
    tbody.innerHTML = '';

    const datos = buscarCoincidencias(filtro);

    if (datos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted p-5">No se encontraron medicamentos registrados.</td></tr>`;
        return;
    }

    datos.forEach((med, index) => {
        const valorTotal = med.stock * med.precio;
        let badgeEstado = '<span class="badge badge-success">En Stock</span>';
        if (med.stock === 0) {
            badgeEstado = '<span class="badge badge-danger">Agotado</span>';
        } else if (med.stock <= 10) {
            badgeEstado = '<span class="badge badge-warning">Stock Bajo</span>';
        }

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>#${index + 1}</strong></td>
            <td><strong style="color: #fff;">${med.nombre}</strong></td>
            <td>$${med.precio.toFixed(2)}</td>
            <td>${med.stock} uds.</td>
            <td><strong style="color: var(--accent-emerald);">$${valorTotal.toFixed(2)}</strong></td>
            <td>${badgeEstado}</td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="irAActualizar('${med.nombre}')" title="Modificar precio o stock">✏️ Editar</button>
                <button class="btn btn-outline btn-sm style='color: var(--danger);'" onclick="irAEliminar('${med.nombre}')" title="Eliminar del catálogo">🗑️</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * Renderiza las tarjetas de búsqueda en la pestaña 2.
 */
function renderizarBusqueda(texto = '') {
    const contenedor = document.getElementById('resultadosBusqueda');
    contenedor.innerHTML = '';

    const resultados = buscarCoincidencias(texto);

    if (resultados.length === 0) {
        contenedor.innerHTML = `<div class="glass-card p-5 text-center text-muted" style="grid-column: 1 / -1;">No se encontraron medicamentos con el término "${texto}".</div>`;
        return;
    }

    resultados.forEach(med => {
        const card = document.createElement('div');
        card.className = 'med-card';
        card.innerHTML = `
            <div>
                <div class="med-card-header">
                    <span class="med-card-title">${med.nombre}</span>
                    <span class="med-card-price">$${med.precio.toFixed(2)}</span>
                </div>
                <p class="text-muted">Stock disponible: <strong>${med.stock}</strong> unidades</p>
                <p class="text-muted text-sm">Valor acumulado: $${(med.stock * med.precio).toFixed(2)}</p>
            </div>
            <div class="med-card-footer">
                <button class="btn btn-outline btn-sm" onclick="irAActualizar('${med.nombre}')">🔄 Actualizar</button>
                <button class="btn btn-primary btn-sm" onclick="irAPedidoConMed('${med.nombre}')">🛒 Vender</button>
            </div>
        `;
        contenedor.appendChild(card);
    });
}

/**
 * Llena las listas desplegables (<select>) con los medicamentos del inventario.
 */
function llenarSelectsMedicamentos() {
    const selects = [
        document.getElementById('selectActualizarMed'),
        document.getElementById('selectEliminarMed'),
        document.getElementById('posSelectMed')
    ];

    selects.forEach(sel => {
        if (!sel) return;
        const valorActual = sel.value;
        sel.innerHTML = '<option value="">-- Seleccione un medicamento --</option>';
        inventario.forEach(med => {
            const opt = document.createElement('option');
            opt.value = med.nombre;
            opt.textContent = `${med.nombre} ($${med.precio.toFixed(2)} | Stock: ${med.stock})`;
            sel.appendChild(opt);
        });
        sel.value = valorActual;
    });
}

/**
 * Renderiza la tabla del Historial General de Pedidos y Ventas en la pestaña 7.
 */
function renderizarTablaHistorial(filtro = '') {
    const tbody = document.getElementById('tablaHistorialBody');
    tbody.innerHTML = '';

    const query = filtro.trim().toLowerCase();
    const datosFiltrados = query ? historialPedidos.filter(row => {
        return row[0].toLowerCase().includes(query) || row[2].toLowerCase().includes(query);
    }) : historialPedidos;

    if (datosFiltrados.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-center text-muted p-5">No hay registros de pedidos en el historial.</td></tr>`;
        return;
    }

    // Renderizamos en orden inverso (más reciente primero)
    datosFiltrados.slice().reverse().forEach((row, index) => {
        const cliente = row[0];
        const cantidad = row[1];
        const nombreMed = row[2];
        const precioUnit = parseFloat(row[3]);
        const subtotal = cantidad * precioUnit;
        const fecha = row[4] || 'N/A';

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><span class="text-muted text-sm">${fecha}</span></td>
            <td><strong style="color: #93c5fd;">${cliente}</strong></td>
            <td><strong style="color: #fff;">${nombreMed}</strong></td>
            <td>${cantidad} uds.</td>
            <td>$${precioUnit.toFixed(2)}</td>
            <td><strong style="color: var(--accent-emerald);">$${subtotal.toFixed(2)}</strong></td>
        `;
        tbody.appendChild(tr);
    });
}

/**
 * Renderiza todos los paneles y listas del sistema.
 */
function renderizarTodo() {
    renderizarTablaInventario();
    renderizarBusqueda();
    llenarSelectsMedicamentos();
    renderizarTablaHistorial();
}


// ============================================================================
// 5. GESTIÓN DEL PUNTO DE VENTA (POS / CREAR PEDIDO)
// ============================================================================

function iniciarNuevoPedido(clienteNombre) {
    if (!clienteNombre || clienteNombre.trim() === '') return;
    pedidoActual = new Pedido(clienteNombre.trim());
    document.getElementById('cartClienteDisplay').textContent = pedidoActual.cliente;
    renderizarCarrito();
    document.getElementById('btnConfirmarPedido').disabled = true;
    document.getElementById('btnLimpiarCarrito').disabled = false;
}

function renderizarCarrito() {
    const tbody = document.getElementById('tablaCarritoBody');
    const totalDisplay = document.getElementById('cartTotalDisplay');
    const btnConfirmar = document.getElementById('btnConfirmarPedido');

    if (!pedidoActual || pedidoActual.medicamentos.length === 0) {
        tbody.innerHTML = `<tr class="empty-row"><td colspan="5" class="text-center text-muted p-4">El pedido está vacío. Agregue productos.</td></tr>`;
        totalDisplay.textContent = '$0.00';
        if (btnConfirmar) btnConfirmar.disabled = true;
        return;
    }

    tbody.innerHTML = '';
    pedidoActual.medicamentos.forEach((item, idx) => {
        const med = item.medicamento;
        const cant = item.cantidad;
        const subtotal = med.precio * cant;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${med.nombre}</strong></td>
            <td>${cant}</td>
            <td>$${med.precio.toFixed(2)}</td>
            <td><strong>$${subtotal.toFixed(2)}</strong></td>
            <td>
                <button type="button" class="btn btn-outline btn-sm" onclick="removerDelCarrito(${idx})" title="Eliminar ítem">❌</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    const total = pedidoActual.calcularTotal();
    totalDisplay.textContent = `$${total.toFixed(2)}`;
    if (btnConfirmar) btnConfirmar.disabled = false;
}

function removerDelCarrito(index) {
    if (!pedidoActual) return;
    const item = pedidoActual.medicamentos[index];
    // Devolvemos el stock al inventario en memoria al quitar del carrito
    item.medicamento.stock += item.cantidad;
    pedidoActual.medicamentos.splice(index, 1);
    renderizarCarrito();
    llenarSelectsMedicamentos();
    renderizarTablaInventario();
    mostrarToast(`Se removió ${item.medicamento.nombre} del pedido.`, 'warning');
}


// ============================================================================
// 6. NAVEGACIÓN Y EVENT LISTENERS
// ============================================================================

function cambiarPestaña(tabId) {
    // Desactivar todos los nav-items y paneles
    document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));

    // Activar el seleccionado
    const btnActivo = document.querySelector(`[data-tab="${tabId}"]`);
    const panelActivo = document.getElementById(tabId);

    if (btnActivo && panelActivo) {
        btnActivo.classList.add('active');
        panelActivo.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Funciones para saltos rápidos desde botones en tarjetas o tablas
window.irAActualizar = function(nombreMed) {
    cambiarPestaña('tab-actualizar');
    const select = document.getElementById('selectActualizarMed');
    if (select) {
        select.value = nombreMed;
        select.dispatchEvent(new Event('change'));
    }
};

window.irAEliminar = function(nombreMed) {
    cambiarPestaña('tab-eliminar');
    const select = document.getElementById('selectEliminarMed');
    if (select) {
        select.value = nombreMed;
        select.dispatchEvent(new Event('change'));
    }
};

window.irAPedidoConMed = function(nombreMed) {
    cambiarPestaña('tab-pedido');
    const select = document.getElementById('posSelectMed');
    if (select) {
        select.value = nombreMed;
        select.dispatchEvent(new Event('change'));
    }
};

/**
 * Muestra alertas visuales estilo Toast notification.
 */
function mostrarToast(mensaje, tipo = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    
    let icono = 'ℹ️';
    if (tipo === 'success') icono = '✅';
    if (tipo === 'error') icono = '❌';
    if (tipo === 'warning') icono = '⚠️';

    toast.innerHTML = `
        <span class="toast-icon">${icono}</span>
        <span class="toast-msg">${mensaje}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(50px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}


// ============================================================================
// 7. INICIALIZACIÓN GENERAL DEL DOM
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Cargar datos en memoria
    cargarDatos();
    actualizarKPIs();
    renderizarTodo();

    // 2. Eventos de la barra de navegación lateral
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            cambiarPestaña(tabId);
        });
    });

    // 3. Botón de restablecer datos
    document.getElementById('btnResetData').addEventListener('click', restablecerDatosDemo);

    // 4. Pestaña 1: Filtro de inventario
    document.getElementById('filterInventario').addEventListener('input', (e) => {
        renderizarTablaInventario(e.target.value);
    });

    // 5. Pestaña 2: Búsqueda en tiempo real
    document.getElementById('inputBuscarMed').addEventListener('input', (e) => {
        renderizarBusqueda(e.target.value);
    });

    // 6. Pestaña 3: Registrar nuevo medicamento
    document.getElementById('formRegistrar').addEventListener('submit', (e) => {
        e.preventDefault();
        const nombre = document.getElementById('regNombre').value.trim();
        const precio = parseFloat(document.getElementById('regPrecio').value);
        const stock = parseInt(document.getElementById('regStock').value, 10);

        if (buscarPorNombre(nombre)) {
            mostrarToast(`El medicamento "${nombre}" ya está registrado en el inventario.`, 'error');
            return;
        }

        const nuevo = new Medicamento(stock, nombre, precio);
        inventario.push(nuevo);
        guardarDatos();
        renderizarTodo();

        mostrarToast(`¡${nombre} registrado exitosamente!`, 'success');
        e.target.reset();
        cambiarPestaña('tab-inventario');
    });

    // 7. Pestaña 4: Selección para actualizar medicamento
    const selectAct = document.getElementById('selectActualizarMed');
    const infoAct = document.getElementById('infoMedActualizar');
    const opcAct = document.getElementById('opcionesActualizar');

    selectAct.addEventListener('change', () => {
        const nombre = selectAct.value;
        const med = buscarPorNombre(nombre);

        if (!med) {
            infoAct.classList.add('hidden');
            opcAct.classList.add('hidden');
            return;
        }

        infoAct.innerHTML = `<strong>Medicamento Seleccionado:</strong> ${med.nombre} &nbsp;|&nbsp; <strong>Precio Actual:</strong> $${med.precio.toFixed(2)} &nbsp;|&nbsp; <strong>Stock Disponible:</strong> ${med.stock} uds.`;
        infoAct.classList.remove('hidden');
        opcAct.classList.remove('hidden');
    });

    // Actualizar Precio
    document.getElementById('formActPrecio').addEventListener('submit', (e) => {
        e.preventDefault();
        const med = buscarPorNombre(selectAct.value);
        if (!med) return;
        const nuevoPrecio = parseFloat(document.getElementById('actNuevoPrecio').value);
        med.precio = nuevoPrecio;
        guardarDatos();
        renderizarTodo();
        selectAct.dispatchEvent(new Event('change'));
        document.getElementById('actNuevoPrecio').value = '';
        mostrarToast(`Precio de ${med.nombre} actualizado a $${nuevoPrecio.toFixed(2)}.`, 'success');
    });

    // Actualizar Stock
    document.getElementById('formActStock').addEventListener('submit', (e) => {
        e.preventDefault();
        const med = buscarPorNombre(selectAct.value);
        if (!med) return;
        const nuevoStock = parseInt(document.getElementById('actNuevoStock').value, 10);
        med.stock = nuevoStock;
        guardarDatos();
        renderizarTodo();
        selectAct.dispatchEvent(new Event('change'));
        document.getElementById('actNuevoStock').value = '';
        mostrarToast(`Stock de ${med.nombre} actualizado a ${nuevoStock} unidades.`, 'success');
    });

    // Aplicar Descuento
    document.getElementById('formActDescuento').addEventListener('submit', (e) => {
        e.preventDefault();
        const med = buscarPorNombre(selectAct.value);
        if (!med) return;
        const porcentaje = parseFloat(document.getElementById('actPorcentaje').value);
        const msg = med.aplicarDescuento(porcentaje);
        guardarDatos();
        renderizarTodo();
        selectAct.dispatchEvent(new Event('change'));
        document.getElementById('actPorcentaje').value = '';
        mostrarToast(msg, 'success');
    });

    // 8. Pestaña 5: Eliminar medicamento
    const selectDel = document.getElementById('selectEliminarMed');
    const previewDel = document.getElementById('previewEliminar');

    selectDel.addEventListener('change', () => {
        const med = buscarPorNombre(selectDel.value);
        if (!med) {
            previewDel.classList.add('hidden');
            return;
        }
        document.getElementById('delNombreMed').textContent = med.nombre;
        document.getElementById('delPrecioMed').textContent = med.precio.toFixed(2);
        document.getElementById('delStockMed').textContent = med.stock;
        previewDel.classList.remove('hidden');
    });

    document.getElementById('btnConfirmarEliminar').addEventListener('click', () => {
        const nombre = selectDel.value;
        const med = buscarPorNombre(nombre);
        if (!med) return;

        inventario = inventario.filter(m => m.nombre !== nombre);
        guardarDatos();
        renderizarTodo();
        previewDel.classList.add('hidden');
        mostrarToast(`Medicamento "${nombre}" eliminado del catálogo.`, 'warning');
    });

    // 9. Pestaña 6: POS (Crear Pedido / Venta)
    const inputCliente = document.getElementById('posCliente');
    const selectPosMed = document.getElementById('posSelectMed');
    const posMedDetalle = document.getElementById('posMedDetalle');

    inputCliente.addEventListener('change', () => {
        const cli = inputCliente.value.trim();
        if (cli) {
            if (!pedidoActual || pedidoActual.cliente !== cli) {
                iniciarNuevoPedido(cli);
            }
        }
    });

    selectPosMed.addEventListener('change', () => {
        const med = buscarPorNombre(selectPosMed.value);
        if (!med) {
            posMedDetalle.classList.add('hidden');
            return;
        }
        posMedDetalle.innerHTML = `Precio Unitario: <strong>$${med.precio.toFixed(2)}</strong> &nbsp;|&nbsp; Stock Disponible: <strong>${med.stock}</strong> uds.`;
        posMedDetalle.classList.remove('hidden');
        document.getElementById('posCantidad').max = med.stock;
        document.getElementById('posCantidad').value = 1;
    });

    document.getElementById('btnAgregarAlCarrito').addEventListener('click', () => {
        const cli = inputCliente.value.trim();
        if (!cli) {
            mostrarToast('Por favor, ingrese el nombre del cliente primero.', 'error');
            inputCliente.focus();
            return;
        }

        if (!pedidoActual || pedidoActual.cliente !== cli) {
            iniciarNuevoPedido(cli);
        }

        const med = buscarPorNombre(selectPosMed.value);
        if (!med) {
            mostrarToast('Seleccione un medicamento disponible de la lista.', 'error');
            return;
        }

        const cant = parseInt(document.getElementById('posCantidad').value, 10);
        if (isNaN(cant) || cant <= 0) {
            mostrarToast('Ingrese una cantidad válida mayor a 0.', 'error');
            return;
        }

        if (cant > med.stock) {
            mostrarToast(`No hay suficiente stock de ${med.nombre}. Disponible: ${med.stock} unidades.`, 'error');
            return;
        }

        try {
            pedidoActual.agregarMedicamento(med, cant);
            renderizarCarrito();
            llenarSelectsMedicamentos();
            renderizarTablaInventario();
            mostrarToast(`Agregado: ${cant}x ${med.nombre} al pedido de ${cli}.`, 'success');
            selectPosMed.value = '';
            posMedDetalle.classList.add('hidden');
        } catch (err) {
            mostrarToast(err.message, 'error');
        }
    });

    document.getElementById('btnLimpiarCarrito').addEventListener('click', () => {
        if (!pedidoActual) return;
        // Devolver stocks
        pedidoActual.medicamentos.forEach(item => {
            item.medicamento.stock += item.cantidad;
        });
        pedidoActual.medicamentos = [];
        renderizarCarrito();
        llenarSelectsMedicamentos();
        renderizarTablaInventario();
        mostrarToast('Pedido vaciado.', 'info');
    });

    document.getElementById('btnConfirmarPedido').addEventListener('click', () => {
        if (!pedidoActual || pedidoActual.medicamentos.length === 0) {
            mostrarToast('No hay medicamentos en el pedido.', 'error');
            return;
        }

        // Agregar al historial global
        const filas = pedidoActual.aFilasRegistro();
        historialPedidos.push(...filas);

        // Guardar cambios en persistencia (localStorage)
        guardarDatos();
        renderizarTodo();

        mostrarToast(`¡Pedido de "${pedidoActual.cliente}" por $${pedidoActual.calcularTotal().toFixed(2)} registrado exitosamente!`, 'success');
        
        // Reiniciar POS
        pedidoActual = null;
        inputCliente.value = '';
        document.getElementById('cartClienteDisplay').textContent = 'No especificado';
        renderizarCarrito();
        cambiarPestaña('tab-historial');
    });

    // 10. Pestaña 7: Filtro de historial
    document.getElementById('filterHistorial').addEventListener('input', (e) => {
        renderizarTablaHistorial(e.target.value);
    });
});
