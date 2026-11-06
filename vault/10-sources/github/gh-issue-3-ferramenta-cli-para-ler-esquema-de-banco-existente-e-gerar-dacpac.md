---
id: "gh-issue-3"
title: "ferramenta cli para ler esquema de banco existente e gerar dacpac"
kind: "research-source"
domain: "uncategorized"
tags:
  - "domain/uncategorized"
  - "source/ai"
ai_provider: "Unknown"
source_issue: 3
source_url: "https://github.com/DevComputaria/knowledge-vault/issues/3"
created: "2026-11-06"
status: "captured"
evidence_status: "unverified"
---

# ferramenta cli para ler esquema de banco existente e gerar dacpac

> [!info] Proveniência
> Captura integral da Issue [#3](https://github.com/DevComputaria/knowledge-vault/issues/3). O conteúdo e as referências ainda não foram verificados.

**Domínio:** [[../../30-mocs/domain-uncategorized|uncategorized]]

## Pesquisa original

**Na lista anterior, não. A CLI adequada para ler o esquema de um SQL Server existente e gerar um `.dacpac` é o Microsoft SqlPackage**, usando a ação `Extract`. Não precisa de MCP nem de Copilot.

O **Data API Builder** expõe dados por APIs; o **SqlPackage** extrai e implanta modelos de esquema.

### Instalação

Com o SDK do .NET compatível instalado:

```bash
dotnet tool install --global Microsoft.SqlPackage
```

A ferramenta está disponível para Windows, Linux e macOS. [Referência oficial de instalação](https://learn.microsoft.com/pt-br/fabric/database/sql/sqlpackage).

### Extrair somente o esquema

Exemplo para **Windows com autenticação integrada** — substitua `<SERVIDOR>` e `<BANCO>`:

```powershell
sqlpackage /Action:Extract /SourceConnectionString:"Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" /TargetFile:"esquema.dacpac" /p:ExtractAllTableData=False /p:VerifyExtraction=True
```

Esse comando:

- Conecta-se ao banco existente e lê as definições dos objetos suportados.
- Gera o arquivo local `esquema.dacpac`.
- **Não inclui os registros das tabelas** e não publica alterações no banco de origem.
- Valida o modelo extraído com `VerifyExtraction=True`.

A conta utilizada precisa ter as permissões necessárias para a extração, e o certificado do servidor precisa ser confiável para essa conexão.

**Documentação principal:** [SqlPackage — ação Extract, parâmetros e exemplos](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Você usa Windows com autenticação integrada ou conecta ao SQL Server com usuário e senha?


Se for **usuário do Active Directory de domínio (AD Windows)**, use autenticação integrada. O SqlPackage utiliza a identidade do usuário que está executando o terminal, sem informar senha no comando.

### Extrair o esquema para DACPAC

No Windows, abra o PowerShell com o usuário de domínio autorizado e execute, substituindo `<SERVIDOR>` e `<BANCO>`:

```powershell
sqlpackage /Action:Extract /SourceConnectionString:"Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" /TargetFile:"esquema.dacpac" /p:ExtractAllTableData=False /p:VerifyExtraction=True
```

**Resultado:** arquivo `esquema.dacpac` na pasta atual, contendo o esquema dos objetos suportados, sem os dados das tabelas e sem alterar o banco de origem.

Pontos importantes:
- O usuário AD precisa ter acesso ao SQL Server e permissões para extração.
- O certificado do SQL Server precisa ser confiável.
- **AD de domínio e Microsoft Entra ID são autenticações diferentes**; se você usa login com MFA, o comando precisa ser ajustado.

[Referência oficial: extração com SqlPackage](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Seu acesso é com conta de domínio, como `DOMINIO\usuario`, ou Microsoft Entra ID com MFA?


**Sim. Para usar sua conta AD de domínio, o caminho mais simples é chamar o SqlPackage do Windows a partir do terminal WSL.** Assim, a autenticação integrada usa a identidade do Windows, sem precisar configurar Kerberos dentro do Linux.

Os comandos abaixo pressupõem **AD Windows, como `DOMINIO\usuario`**, não Microsoft Entra ID com MFA.

### 1. Confira a identidade do Windows pelo WSL

No terminal WSL:

```bash
whoami.exe
```

Confira se aparece a conta de domínio que tem acesso ao SQL Server. O comando Linux `whoami`, sem `.exe`, mostra apenas o usuário do WSL.

Conecte também a VPN corporativa, caso seja necessária para acessar o servidor.

### 2. Instale o SqlPackage no Windows

Ainda no WSL, confirme que o **SDK do .NET do Windows** está instalado:

```bash
powershell.exe -NoProfile -Command 'dotnet --list-sdks'
```

Depois instale:

```bash
powershell.exe -NoProfile -Command 'dotnet tool install --global Microsoft.SqlPackage'
```

Se já estiver instalado, atualize:

```bash
powershell.exe -NoProfile -Command 'dotnet tool update --global Microsoft.SqlPackage'
```

**Importante:** executar apenas `dotnet` no WSL pode usar a instalação Linux. Aqui usamos `powershell.exe` para instalar e executar no Windows.

[Instalação oficial do SqlPackage](https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download?view=sql-server-ver16).

### 3. Valide o executável

Para a instalação global feita acima:

```bash
powershell.exe -NoProfile -Command '& "$env:USERPROFILE\.dotnet\tools\sqlpackage.exe" /Version'
```

### 4. Extraia o DACPAC com autenticação AD

Substitua `<SERVIDOR>` e `<BANCO>` e execute **no WSL**:

```bash
powershell.exe -NoProfile -Command '
& "$env:USERPROFILE\.dotnet\tools\sqlpackage.exe" `
  /Action:Extract `
  "/SourceConnectionString:Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" `
  "/TargetFile:$env:USERPROFILE\esquema.dacpac" `
  /p:ExtractAllTableData=False `
  /p:VerifyExtraction=True
exit $LASTEXITCODE
'
```

O arquivo será salvo na **pasta do seu usuário Windows**, com o nome `esquema.dacpac`.

A operação extrai o esquema dos objetos suportados, **sem os registros das tabelas e sem publicar alterações no banco**.

### Se ocorrer erro

- **Login failed:** confira a identidade mostrada por `whoami.exe` e as permissões de extração.
- **Servidor não encontrado ou timeout:** confira nome, instância/porta, VPN e acesso de rede.
- **Certificado não confiável:** solicite a configuração da cadeia de confiança corporativa; o comando mantém a validação TLS habilitada.

**Executar o SqlPackage nativo do Linux no WSL é outro cenário:** o login AD do Windows não é herdado automaticamente para autenticação integrada; normalmente é necessário configurar Kerberos.

[Referência oficial da ação Extract](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Quer que eu adapte o comando para uma instância nomeada ou uma porta específica?

## Referências informadas

Nenhuma referência informada.

## Captura bruta da Issue

<details>
<summary>Exibir corpo original</summary>

**Na lista anterior, não. A CLI adequada para ler o esquema de um SQL Server existente e gerar um `.dacpac` é o Microsoft SqlPackage**, usando a ação `Extract`. Não precisa de MCP nem de Copilot.

O **Data API Builder** expõe dados por APIs; o **SqlPackage** extrai e implanta modelos de esquema.

### Instalação

Com o SDK do .NET compatível instalado:

```bash
dotnet tool install --global Microsoft.SqlPackage
```

A ferramenta está disponível para Windows, Linux e macOS. [Referência oficial de instalação](https://learn.microsoft.com/pt-br/fabric/database/sql/sqlpackage).

### Extrair somente o esquema

Exemplo para **Windows com autenticação integrada** — substitua `<SERVIDOR>` e `<BANCO>`:

```powershell
sqlpackage /Action:Extract /SourceConnectionString:"Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" /TargetFile:"esquema.dacpac" /p:ExtractAllTableData=False /p:VerifyExtraction=True
```

Esse comando:

- Conecta-se ao banco existente e lê as definições dos objetos suportados.
- Gera o arquivo local `esquema.dacpac`.
- **Não inclui os registros das tabelas** e não publica alterações no banco de origem.
- Valida o modelo extraído com `VerifyExtraction=True`.

A conta utilizada precisa ter as permissões necessárias para a extração, e o certificado do servidor precisa ser confiável para essa conexão.

**Documentação principal:** [SqlPackage — ação Extract, parâmetros e exemplos](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Você usa Windows com autenticação integrada ou conecta ao SQL Server com usuário e senha?


Se for **usuário do Active Directory de domínio (AD Windows)**, use autenticação integrada. O SqlPackage utiliza a identidade do usuário que está executando o terminal, sem informar senha no comando.

### Extrair o esquema para DACPAC

No Windows, abra o PowerShell com o usuário de domínio autorizado e execute, substituindo `<SERVIDOR>` e `<BANCO>`:

```powershell
sqlpackage /Action:Extract /SourceConnectionString:"Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" /TargetFile:"esquema.dacpac" /p:ExtractAllTableData=False /p:VerifyExtraction=True
```

**Resultado:** arquivo `esquema.dacpac` na pasta atual, contendo o esquema dos objetos suportados, sem os dados das tabelas e sem alterar o banco de origem.

Pontos importantes:
- O usuário AD precisa ter acesso ao SQL Server e permissões para extração.
- O certificado do SQL Server precisa ser confiável.
- **AD de domínio e Microsoft Entra ID são autenticações diferentes**; se você usa login com MFA, o comando precisa ser ajustado.

[Referência oficial: extração com SqlPackage](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Seu acesso é com conta de domínio, como `DOMINIO\usuario`, ou Microsoft Entra ID com MFA?


**Sim. Para usar sua conta AD de domínio, o caminho mais simples é chamar o SqlPackage do Windows a partir do terminal WSL.** Assim, a autenticação integrada usa a identidade do Windows, sem precisar configurar Kerberos dentro do Linux.

Os comandos abaixo pressupõem **AD Windows, como `DOMINIO\usuario`**, não Microsoft Entra ID com MFA.

### 1. Confira a identidade do Windows pelo WSL

No terminal WSL:

```bash
whoami.exe
```

Confira se aparece a conta de domínio que tem acesso ao SQL Server. O comando Linux `whoami`, sem `.exe`, mostra apenas o usuário do WSL.

Conecte também a VPN corporativa, caso seja necessária para acessar o servidor.

### 2. Instale o SqlPackage no Windows

Ainda no WSL, confirme que o **SDK do .NET do Windows** está instalado:

```bash
powershell.exe -NoProfile -Command 'dotnet --list-sdks'
```

Depois instale:

```bash
powershell.exe -NoProfile -Command 'dotnet tool install --global Microsoft.SqlPackage'
```

Se já estiver instalado, atualize:

```bash
powershell.exe -NoProfile -Command 'dotnet tool update --global Microsoft.SqlPackage'
```

**Importante:** executar apenas `dotnet` no WSL pode usar a instalação Linux. Aqui usamos `powershell.exe` para instalar e executar no Windows.

[Instalação oficial do SqlPackage](https://learn.microsoft.com/en-us/sql/tools/sqlpackage/sqlpackage-download?view=sql-server-ver16).

### 3. Valide o executável

Para a instalação global feita acima:

```bash
powershell.exe -NoProfile -Command '& "$env:USERPROFILE\.dotnet\tools\sqlpackage.exe" /Version'
```

### 4. Extraia o DACPAC com autenticação AD

Substitua `<SERVIDOR>` e `<BANCO>` e execute **no WSL**:

```bash
powershell.exe -NoProfile -Command '
& "$env:USERPROFILE\.dotnet\tools\sqlpackage.exe" `
  /Action:Extract `
  "/SourceConnectionString:Server=<SERVIDOR>;Database=<BANCO>;Integrated Security=True;Encrypt=True;TrustServerCertificate=False" `
  "/TargetFile:$env:USERPROFILE\esquema.dacpac" `
  /p:ExtractAllTableData=False `
  /p:VerifyExtraction=True
exit $LASTEXITCODE
'
```

O arquivo será salvo na **pasta do seu usuário Windows**, com o nome `esquema.dacpac`.

A operação extrai o esquema dos objetos suportados, **sem os registros das tabelas e sem publicar alterações no banco**.

### Se ocorrer erro

- **Login failed:** confira a identidade mostrada por `whoami.exe` e as permissões de extração.
- **Servidor não encontrado ou timeout:** confira nome, instância/porta, VPN e acesso de rede.
- **Certificado não confiável:** solicite a configuração da cadeia de confiança corporativa; o comando mantém a validação TLS habilitada.

**Executar o SqlPackage nativo do Linux no WSL é outro cenário:** o login AD do Windows não é herdado automaticamente para autenticação integrada; normalmente é necessário configurar Kerberos.

[Referência oficial da ação Extract](https://learn.microsoft.com/pt-br/sql/tools/sqlpackage/sqlpackage-extract?view=sql-server-ver17).

Quer que eu adapte o comando para uma instância nomeada ou uma porta específica?

</details>
