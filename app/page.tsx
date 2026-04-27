"use client";

import { useState } from "react";

export default function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState<{
    status: string;
    probabilidade: number;
  } | null>(null);
  const [erro, setErro] = useState<string | null>(null);

  // Estado para guardar os dados do formulário
  const [formData, setFormData] = useState({
    studytime: 2,
    failures: 0,
    absences: 0,
    G1: 12,
    G2: 12,
  });

  // Função que envia os dados para a nossa API Python
  const handlePrevisao = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/prever", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          studytime: Number(formData.studytime),
          failures: Number(formData.failures),
          absences: Number(formData.absences),
          G1: Number(formData.G1),
          G2: Number(formData.G2),
        }),
      });

      if (!response.ok) throw new Error("Falha ao conectar com a API de IA");

      const data = await response.json();
      setResultado({
        status: data.status,
        probabilidade: data.probabilidade,
      });
    } catch (error) {
      setErro(
        "Erro de conexão. Verifique se a API Python está rodando na porta 8000.",
      );
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8 text-gray-800">
      <div className="max-w-5xl mx-auto">
        <header className="mb-10">
          <h1 className="text-3xl font-bold text-blue-900">EducaPrev</h1>
          <p className="text-gray-600">
            Sistema Inteligente de Previsão de Desempenho Escolar
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Formulário de Input */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-4 border-b pb-2">
              Dados do Aluno
            </h2>
            <form onSubmit={handlePrevisao} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Tempo de Estudo Semanal
                </label>
                <select
                  name="studytime"
                  value={formData.studytime}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2 bg-gray-50"
                >
                  <option value={1}>&lt; 2 horas</option>
                  <option value={2}>2 a 5 horas</option>
                  <option value={3}>5 a 10 horas</option>
                  <option value={4}>&gt; 10 horas</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">
                  Reprovações Anteriores (0 a 3)
                </label>
                <input
                  type="number"
                  name="failures"
                  min="0"
                  max="3"
                  value={formData.failures}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2 bg-gray-50"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">
                  Total de Faltas
                </label>
                <input
                  type="number"
                  name="absences"
                  min="0"
                  value={formData.absences}
                  onChange={handleChange}
                  className="w-full border rounded-lg p-2 bg-gray-50"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">
                    Nota 1º Bimestre (0-20)
                  </label>
                  <input
                    type="number"
                    name="G1"
                    min="0"
                    max="20"
                    step="0.1"
                    value={formData.G1}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2 bg-gray-50"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">
                    Nota 2º Bimestre (0-20)
                  </label>
                  <input
                    type="number"
                    name="G2"
                    min="0"
                    max="20"
                    step="0.1"
                    value={formData.G2}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2 bg-gray-50"
                    required
                  />
                </div>
              </div>

              {erro && <p className="text-red-500 text-sm mt-2">{erro}</p>}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors mt-4"
              >
                {loading
                  ? "Analisando pelo Modelo..."
                  : "Gerar Previsão com IA"}
              </button>
            </form>
          </div>

          {/* Painel de Resultado */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-center items-center text-center">
            {resultado ? (
              <div className="animate-fade-in w-full">
                <h2 className="text-2xl font-bold mb-4">
                  Análise da Rede Neural
                </h2>
                <div
                  className={`p-6 rounded-lg border-2 ${resultado.probabilidade > 50 ? "bg-red-50 border-red-200 text-red-700" : "bg-green-50 border-green-200 text-green-700"}`}
                >
                  <p className="text-2xl font-bold mb-2">{resultado.status}</p>
                  <div className="w-full bg-gray-200 rounded-full h-4 mb-2 mt-4">
                    <div
                      className={`h-4 rounded-full ${resultado.probabilidade > 50 ? "bg-red-500" : "bg-green-500"}`}
                      style={{ width: `${resultado.probabilidade}%` }}
                    ></div>
                  </div>
                  <p className="text-sm mt-1 font-semibold">
                    Probabilidade de Risco: {resultado.probabilidade}%
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-gray-400">
                <svg
                  className="w-16 h-16 mx-auto mb-4 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  ></path>
                </svg>
                <p>
                  Preencha os dados do aluno e acione o modelo de IA para gerar
                  a previsão.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
