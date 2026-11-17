const $ = (id) => document.getElementById(id);
const feedback = $("feedback");
function avisar(mensagem, erro = false) {
  feedback.textContent = mensagem;
  feedback.style.borderLeftColor = erro ? "#b42318" : "";
}
async function requisicao(url, opcoes = {}) {
  const resposta = await fetch(url, {headers: {"Content-Type":"application/json"}, ...opcoes});
  const dados = await resposta.json();
  if (!resposta.ok) throw new Error(dados.erro || "Não foi possível concluir a operação.");
  return dados;
}
function adicionarCelula(linha, valor) {
  const celula = document.createElement("td");
  celula.textContent = valor;
  linha.appendChild(celula);
}
async function carregarDados() {
  const [clientes, ordens] = await Promise.all([requisicao("/clientes"), requisicao("/os")]);
  $("total-clientes").textContent = clientes.length;
  $("total-os").textContent = ordens.length;
  $("total-abertas").textContent = ordens.filter(os => os.status === "Aberta").length;
  const seletor = $("cliente_id");
  const selecionado = seletor.value;
  seletor.replaceChildren(new Option("Selecione um cliente", ""));
  clientes.forEach(cliente => seletor.add(new Option(cliente.nome, cliente.id)));
  if (clientes.some(cliente => String(cliente.id) === selecionado)) seletor.value = selecionado;
  const corpoClientes = $("clientes-lista");
  corpoClientes.replaceChildren();
  if (!clientes.length) {
    const linha = corpoClientes.insertRow(); const celula = linha.insertCell(); celula.colSpan=3; celula.textContent="Nenhum cliente cadastrado.";
  } else clientes.forEach(cliente => {
    const linha=corpoClientes.insertRow(); adicionarCelula(linha, cliente.id); adicionarCelula(linha, cliente.nome); adicionarCelula(linha, cliente.email);
  });
  const corpoOS = $("os-lista"); corpoOS.replaceChildren();
  if (!ordens.length) {
    const linha=corpoOS.insertRow(); const celula=linha.insertCell(); celula.colSpan=4; celula.textContent="Nenhuma ordem registrada.";
  } else ordens.forEach(os => {
    const cliente=clientes.find(item => item.id === os.cliente_id);
    const linha=corpoOS.insertRow(); adicionarCelula(linha, os.id); adicionarCelula(linha, cliente ? cliente.nome : "Cliente"); adicionarCelula(linha, os.descricao);
    const status=linha.insertCell(); const etiqueta=document.createElement("span"); etiqueta.className="status"; etiqueta.textContent=os.status; status.appendChild(etiqueta);
  });
}
$("cliente-form").addEventListener("submit", async evento => {
  evento.preventDefault();
  const formulario=evento.currentTarget;
  const dados=Object.fromEntries(new FormData(formulario));
  try { await requisicao("/clientes",{method:"POST",body:JSON.stringify(dados)}); formulario.reset(); await carregarDados(); avisar("Cliente cadastrado com sucesso."); }
  catch(erro) { avisar(erro.message,true); }
});
$("os-form").addEventListener("submit", async evento => {
  evento.preventDefault();
  const formulario=evento.currentTarget;
  const dados=Object.fromEntries(new FormData(formulario));
  try { await requisicao("/os",{method:"POST",body:JSON.stringify(dados)}); formulario.reset(); await carregarDados(); avisar("Ordem de serviço registrada com sucesso."); }
  catch(erro) { avisar(erro.message,true); }
});
const botaoContraste=$("contrast-toggle");
function aplicarContraste(ativo) {
  document.body.classList.toggle("high-contrast",ativo);
  botaoContraste.setAttribute("aria-pressed",String(ativo));
  botaoContraste.textContent=ativo ? "Alto contraste: ligado" : "Alto contraste: desligado";
  try { localStorage.setItem("techfix-alto-contraste",String(ativo)); } catch (_) {}
}
let contrasteSalvo=false;
try { contrasteSalvo=localStorage.getItem("techfix-alto-contraste")==="true"; } catch (_) {}
aplicarContraste(contrasteSalvo);
botaoContraste.addEventListener("click",()=>aplicarContraste(!document.body.classList.contains("high-contrast")));
carregarDados().catch(erro=>avisar("Não foi possível carregar os dados: "+erro.message,true));