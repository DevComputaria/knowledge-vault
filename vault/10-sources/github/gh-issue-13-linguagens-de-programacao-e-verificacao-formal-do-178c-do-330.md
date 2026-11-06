---
id: "gh-issue-13"
title: "Linguagens de Programação e Verificação Formal (DO-178C / DO-330)"
kind: "research-source"
domain: "uncategorized"
tags:
  - "domain/uncategorized"
  - "source/ai"
ai_provider: "Unknown"
source_issue: 13
source_url: "https://github.com/DevComputaria/knowledge-vault/issues/13"
created: "2026-11-06"
status: "captured"
evidence_status: "unverified"
---

# Linguagens de Programação e Verificação Formal (DO-178C / DO-330)

> [!info] Proveniência
> Captura integral da Issue [#13](https://github.com/DevComputaria/knowledge-vault/issues/13). O conteúdo e as referências ainda não foram verificados.

**Domínio:** [[../../30-mocs/domain-uncategorized|uncategorized]]

## Pesquisa original

Aqui estão as últimas atualizações e destaques de mercado no ecossistema de desenvolvimento de software, hardware, padrões e linguagens para a aviação comercial e militar:
1. Linguagens de Programação e Verificação Formal (DO-178C / DO-330)
 * AdaCore & CMU: Verificação Formal em Rust:
   * Em anúncio conjunto entre a AdaCore e pesquisadores da Carnegie Mellon University (CMU), foram formalizados novos métodos para provas formais de programas em Rust voltados a aviônicos e sistemas de alta integridade (safety-critical).
   * O avanço viabiliza a análise matemática estática em Rust similar ao que o SPARK faz para Ada, permitindo provar a ausência de exceções em tempo de execução (absence of run-time errors) e estender o uso do Rust para além de bibliotecas periféricas, mirando o nível mais alto de criticidade (DO-178C DAL A).
 * Mapeamento de MC/DC em Rust (GNAT Pro 26.0):
   * O ecossistema GNAT Pro for Rust consolidou a interpretação da métrica MC/DC (Modified Condition/Decision Coverage) para expressões idiomáticas de pattern matching (match com or-patterns e guards).
   * Sob a norma DO-330, o fluxo de compilação via rustc exige apenas o nível de qualificação TQL-5, reduzindo os custos de certificação para código compilado em Rust.
 * MBD e SCADE (DO-331):
   * Ferramentas baseadas em modelos (Model-Based Development), como o Ansys SCADE Suite e Simulink, continuam expandindo geradores automáticos de código C e Ada qualificados sob TQL-1, convertendo modelos funcionais aerodinâmicos diretamente em código determinístico em conformidade com a arquitetura aberta FACE™.
2. Cibersegurança Cibernética e Padrões Regulatórios
 * Transição para Cibersegurança Obrigatória (DO-326A / EASA Part-IS):
   * Com o aumento dos ataques a infraestruturas aéreas e de telemetria, o EASA e a FAA passaram a exigir a implementação do EASA Part-IS e conformidade estrita com a DO-326A / ED-202A (Airworthiness Security Process Specification).
   * A arquitetura de software de novos aviônicos exige segmentação Zero-Trust no nível de hardware, criptografia de ponta a ponta nos barramentos ACARS / ARINC 429 e isolamento entre redes de cabine (passageiros/IFE) e barramentos de controle de voo.
 * Standardização de Processadores Multi-Core (A(M)C 20-193):
   * Avanço no uso de ferramentas de análise de contensão temporal e isolamento de memória sob partições ARINC 653, permitindo o uso seguro de chips de múltiplos núcleos (Multi-core Processors) em computadores de voo sem comprometer o determinismo.
3. Patentes e Propriedade Intelectual Recentes em Aviônica
 * Transposição de IP Aeroespacial para o Setor Automotivo (Honeywell Aerospace):
   * A Honeywell Aerospace abriu processos de violação de patentes originais de aviação e autonomia contra as montadoras de EV Rivian e Lucid.
   * As patentes cobrem sistemas de segurança que monitoram combinações de estados do veículo em tempo real (US 7,088,264), navegação autônoma por fusão de sensores GPS, inerciais e de imagem (US 7,840,352) e navegação por LiDAR (US 8,364,334) — tecnologias originalmente desenvolvidas para cockpit e piloto automático que agora redefinem o mercado de transporte autônomo.
 * Monitores Flat Panel de Cockpit com Integridade Gráfica:
   * Concessões recentes de patentes internacionais focam no monitoramento continuo da integridade da imagem renderizada em displays multifuncionais de cabine, garantindo que falhas de GPU não exibam atitude ou altitude incorretas para os pilotos sem acionar um sinal de aviso imediato.
4. Hardware e Arquiteturas de Defesa (MOSA / SOSA / RISC-V)
 * Segurança e Funcionalidade em Aviônicos com RISC-V:
   * Publicações e apresentações técnicas do setor apresentaram arquiteturas abertas baseadas em processadores RISC-V certificados para aviônicos de defesa, oferecendo suporte ao padrão SOSA™ / OpenVPX e reduzindo custos com licenças proprietárias.
 * Barramentos SOSA / OpenVPX 200G:
   * Backplanes de alta velocidade (até 56 Gbps por par diferencial) consolidam-se no mercado de defesa para integrar FPGAs de alta densidade e inferência de IA na borda (Edge AI) em aviões de missão e vetores não tripulados (CCAs / Drones).

## Referências informadas

Nenhuma referência informada.

## Captura bruta da Issue

<details>
<summary>Exibir corpo original</summary>

Aqui estão as últimas atualizações e destaques de mercado no ecossistema de desenvolvimento de software, hardware, padrões e linguagens para a aviação comercial e militar:
1. Linguagens de Programação e Verificação Formal (DO-178C / DO-330)
 * AdaCore & CMU: Verificação Formal em Rust:
   * Em anúncio conjunto entre a AdaCore e pesquisadores da Carnegie Mellon University (CMU), foram formalizados novos métodos para provas formais de programas em Rust voltados a aviônicos e sistemas de alta integridade (safety-critical).
   * O avanço viabiliza a análise matemática estática em Rust similar ao que o SPARK faz para Ada, permitindo provar a ausência de exceções em tempo de execução (absence of run-time errors) e estender o uso do Rust para além de bibliotecas periféricas, mirando o nível mais alto de criticidade (DO-178C DAL A).
 * Mapeamento de MC/DC em Rust (GNAT Pro 26.0):
   * O ecossistema GNAT Pro for Rust consolidou a interpretação da métrica MC/DC (Modified Condition/Decision Coverage) para expressões idiomáticas de pattern matching (match com or-patterns e guards).
   * Sob a norma DO-330, o fluxo de compilação via rustc exige apenas o nível de qualificação TQL-5, reduzindo os custos de certificação para código compilado em Rust.
 * MBD e SCADE (DO-331):
   * Ferramentas baseadas em modelos (Model-Based Development), como o Ansys SCADE Suite e Simulink, continuam expandindo geradores automáticos de código C e Ada qualificados sob TQL-1, convertendo modelos funcionais aerodinâmicos diretamente em código determinístico em conformidade com a arquitetura aberta FACE™.
2. Cibersegurança Cibernética e Padrões Regulatórios
 * Transição para Cibersegurança Obrigatória (DO-326A / EASA Part-IS):
   * Com o aumento dos ataques a infraestruturas aéreas e de telemetria, o EASA e a FAA passaram a exigir a implementação do EASA Part-IS e conformidade estrita com a DO-326A / ED-202A (Airworthiness Security Process Specification).
   * A arquitetura de software de novos aviônicos exige segmentação Zero-Trust no nível de hardware, criptografia de ponta a ponta nos barramentos ACARS / ARINC 429 e isolamento entre redes de cabine (passageiros/IFE) e barramentos de controle de voo.
 * Standardização de Processadores Multi-Core (A(M)C 20-193):
   * Avanço no uso de ferramentas de análise de contensão temporal e isolamento de memória sob partições ARINC 653, permitindo o uso seguro de chips de múltiplos núcleos (Multi-core Processors) em computadores de voo sem comprometer o determinismo.
3. Patentes e Propriedade Intelectual Recentes em Aviônica
 * Transposição de IP Aeroespacial para o Setor Automotivo (Honeywell Aerospace):
   * A Honeywell Aerospace abriu processos de violação de patentes originais de aviação e autonomia contra as montadoras de EV Rivian e Lucid.
   * As patentes cobrem sistemas de segurança que monitoram combinações de estados do veículo em tempo real (US 7,088,264), navegação autônoma por fusão de sensores GPS, inerciais e de imagem (US 7,840,352) e navegação por LiDAR (US 8,364,334) — tecnologias originalmente desenvolvidas para cockpit e piloto automático que agora redefinem o mercado de transporte autônomo.
 * Monitores Flat Panel de Cockpit com Integridade Gráfica:
   * Concessões recentes de patentes internacionais focam no monitoramento continuo da integridade da imagem renderizada em displays multifuncionais de cabine, garantindo que falhas de GPU não exibam atitude ou altitude incorretas para os pilotos sem acionar um sinal de aviso imediato.
4. Hardware e Arquiteturas de Defesa (MOSA / SOSA / RISC-V)
 * Segurança e Funcionalidade em Aviônicos com RISC-V:
   * Publicações e apresentações técnicas do setor apresentaram arquiteturas abertas baseadas em processadores RISC-V certificados para aviônicos de defesa, oferecendo suporte ao padrão SOSA™ / OpenVPX e reduzindo custos com licenças proprietárias.
 * Barramentos SOSA / OpenVPX 200G:
   * Backplanes de alta velocidade (até 56 Gbps por par diferencial) consolidam-se no mercado de defesa para integrar FPGAs de alta densidade e inferência de IA na borda (Edge AI) em aviões de missão e vetores não tripulados (CCAs / Drones).

</details>
