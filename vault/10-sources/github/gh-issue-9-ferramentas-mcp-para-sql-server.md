---
id: "gh-issue-9"
title: "Ferramentas MCP para SQL Server"
kind: "research-source"
domain: "uncategorized"
tags:
  - "domain/uncategorized"
  - "source/ai"
ai_provider: "Unknown"
source_issue: 9
source_url: "https://github.com/DevComputaria/knowledge-vault/issues/9"
created: "2026-11-06"
status: "captured"
evidence_status: "unverified"
---

# Ferramentas MCP para SQL Server

> [!info] Proveniência
> Captura integral da Issue [#9](https://github.com/DevComputaria/knowledge-vault/issues/9). O conteúdo e as referências ainda não foram verificados.

**Domínio:** [[../../30-mocs/domain-uncategorized|uncategorized]]

## Pesquisa original

**Resumo direto:**

### 1. Ferramentas MCP para SQL Server

#### Oficial da Microsoft (recomendada para produção)
**SQL MCP Server** (parte do **Data API builder / DAB** a partir da versão 1.7/2.0).

- Não expõe SQL livre (mais seguro).
- Trabalha com **entidades** (tabelas, views, procedures) configuradas em JSON.
- Ferramentas principais: `describe_entities`, `read_records`, `create_record`, `update_record`, `delete_record`, `execute_entity`, `aggregate_records`.
- Suporte a RBAC, cache, telemetria, Entra ID etc.
- Documentação: [learn.microsoft.com/sql/mcp](https://learn.microsoft.com/en-us/sql/mcp/) e Data API builder MCP.

Instalação rápida do CLI:

```bash
dotnet tool install -g microsoft.dataapibuilder
dab init --database-type mssql --connection-string "sua-connection-string" --config dab-config.json
dab add MinhaTabela --source dbo.MinhaTabela --permissions "anonymous:read"
dab start --mcp-stdio
```

#### Comunidade (mais simples, geralmente read-only)

| Projeto | Linguagem | Destaque | Stars aprox. |
|---------|-----------|----------|--------------|
| [RichardHan/mssql_mcp_server](https://github.com/RichardHan/mssql_mcp_server) | Python | Mais popular, read-only por padrão, suporta SQL/Windows/Azure AD | ~400 |
| [bilims/mcp-sqlserver](https://github.com/bilims/mcp-sqlserver) | Node.js | Schema discovery + SELECT seguro | ~46 |
| [jdlemes/MsSqlMCP](https://github.com/jdlemes/MsSqlMCP) | .NET | Schema + queries read-only | - |
| [ian-cowley/MCPSqlServer](https://github.com/ian-cowley/MCPSqlServer) | .NET | Schema + execução de SP | - |
| [ConnorBritain/mssql-mcp-server](https://github.com/ConnorBritain/mssql-mcp-server) | Node.js | Versões reader/writer/admin | - |

Exemplo de config (Claude Desktop / Cursor / etc.) para o mais popular:

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["--from", "microsoft-sql-server-mcp", "mssql_mcp_server"],
      "env": {
        "MSSQL_SERVER": "localhost",
        "MSSQL_DATABASE": "seu_banco",
        "MSSQL_USER": "usuario",
        "MSSQL_PASSWORD": "senha"
      }
    }
  }
}
```

---

### 2. CLI para extrair DACPAC

A ferramenta oficial é o **SqlPackage**.

#### Instalação (recomendada)

```bash
dotnet tool install -g microsoft.sqlpackage
```

(Alternativas: download ZIP standalone no site da Microsoft ou via dbatools no PowerShell.)

#### Extrair DACPAC (schema only – padrão)

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco.dacpac \
  /SourceServerName:localhost \
  /SourceDatabaseName:MeuBanco \
  /SourceUser:usuario \
  /SourcePassword:senha
```

#### Com connection string

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco.dacpac \
  /SourceConnectionString:"Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
```

#### Incluir dados de todas as tabelas

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco_com_dados.dacpac \
  /SourceServerName:localhost \
  /SourceDatabaseName:MeuBanco \
  /p:ExtractAllTableData=true
```

#### Propriedades úteis comuns

| Propriedade | Uso |
|-------------|-----|
| `/p:ExtractAllTableData=true` | Inclui dados de todas as tabelas |
| `/p:IgnorePermissions=true` | Ignora permissões (padrão na maioria dos casos) |
| `/p:IgnoreUserLoginMappings=true` | Ignora mapeamento de logins |
| `/p:VerifyExtraction=true` | Valida o modelo após extração |
| `/p:ExtractTarget=SqlProject` | Extrai como projeto `.sqlproj` em vez de `.dacpac` |

---

### Alternativa PowerShell (dbatools)

```powershell
Install-Module dbatools -Force
Export-DbaDacPackage -SqlInstance "localhost" -Database "MeuBanco" -FilePath "C:\temp\MeuBanco.dacpac"
```

---

**Recomendação prática:**

- Para **agente de IA em produção** → use o **SQL MCP Server oficial** (Data API builder).
- Para exploração rápida de schema + queries → qualquer MCP comunitário read-only.
- Para extrair DACPAC de forma confiável → **SqlPackage** (`dotnet tool`).

Quer que eu monte o `dab-config.json` completo, um script de extração automatizada de vários bancos, ou a config MCP específica para o seu cliente (Cursor, Claude, VS Code etc.)?



Sim. Vou te entregar os três modelos prontos pra usar.

---

### 1. `dab-config.json` completo (SQL MCP Server oficial)

Arquivo de exemplo com tabelas + stored procedure:

```json
{
  "$schema": "https://github.com/Azure/data-api-builder/releases/latest/download/dab.draft.schema.json",
  "data-source": {
    "database-type": "mssql",
    "connection-string": "@env('MSSQL_CONNECTION_STRING')",
    "options": {
      "set-session-context": true
    }
  },
  "runtime": {
    "rest": {
      "enabled": true,
      "path": "/api"
    },
    "graphql": {
      "enabled": true,
      "path": "/graphql"
    },
    "mcp": {
      "enabled": true
    },
    "host": {
      "mode": "development",
      "cors": {
        "origins": ["*"],
        "allow-credentials": false
      },
      "authentication": {
        "provider": "AppService"
      }
    }
  },
  "entities": {
    "Clientes": {
      "source": {
        "object": "dbo.Clientes",
        "type": "table"
      },
      "permissions": [
        {
          "role": "anonymous",
          "actions": ["read"]
        },
        {
          "role": "authenticated",
          "actions": ["create", "read", "update", "delete"]
        }
      ],
      "description": "Cadastro de clientes"
    },
    "Pedidos": {
      "source": {
        "object": "dbo.Pedidos",
        "type": "table"
      },
      "permissions": [
        {
          "role": "authenticated",
          "actions": ["create", "read", "update"]
        }
      ],
      "relationships": {
        "Cliente": {
          "cardinality": "one",
          "target.entity": "Clientes",
          "source.fields": ["ClienteId"],
          "target.fields": ["Id"]
        }
      }
    },
    "ObterPedidoPorId": {
      "source": {
        "object": "dbo.usp_ObterPedidoPorId",
        "type": "stored-procedure"
      },
      "permissions": [
        {
          "role": "authenticated",
          "actions": ["execute"]
        }
      ],
      "mcp": {
        "custom-tool": true
      },
      "description": "Retorna pedido completo por ID"
    }
  }
}
```

**Como subir:**

```bash
# Define a connection string
export MSSQL_CONNECTION_STRING="Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"

# Sobe o MCP em modo stdio (pra Cursor/Claude/VS Code)
dab start --mcp-stdio --config dab-config.json
```

---

### 2. Script de extração de DACPAC (vários bancos)

**PowerShell (Windows / dbatools ou SqlPackage):**

```powershell
# Instala se necessário
# Install-Module dbatools -Force
# dotnet tool install -g microsoft.sqlpackage

$servers = @(
    @{ Server = "localhost"; Databases = @("Banco1", "Banco2", "Banco3") }
    # @{ Server = "outro-servidor"; Databases = @("BancoX") }
)

$outputDir = "C:\Dacpacs\$(Get-Date -Format 'yyyy-MM-dd')"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

foreach ($srv in $servers) {
    foreach ($db in $srv.Databases) {
        $file = Join-Path $outputDir "$($srv.Server.Replace('\','_'))_$db.dacpac"
        
        Write-Host "Extraindo $db de $($srv.Server) -> $file"
        
        # Opção 1: SqlPackage
        sqlpackage /Action:Extract `
            /TargetFile:"$file" `
            /SourceServerName:"$($srv.Server)" `
            /SourceDatabaseName:"$db" `
            /p:IgnorePermissions=true `
            /p:IgnoreUserLoginMappings=true `
            /p:ExtractAllTableData=false
        
        # Opção 2: dbatools (alternativa)
        # Export-DbaDacPackage -SqlInstance $srv.Server -Database $db -FilePath $file
    }
}

Write-Host "Concluído. Arquivos em: $outputDir"
```

**Bash (Linux/macOS + SqlPackage):**

```bash
#!/bin/bash
OUTPUT_DIR="./dacpacs/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

SERVERS=(
  "localhost:Banco1 Banco2 Banco3"
  # "outro-servidor:BancoX"
)

for entry in "${SERVERS[@]}"; do
  SERVER="${entry%%:*}"
  DBS="${entry#*:}"
  
  for DB in $DBS; do
    FILE="$OUTPUT_DIR/${SERVER}_${DB}.dacpac"
    echo "Extraindo $DB de $SERVER -> $FILE"
    
    sqlpackage /Action:Extract \
      /TargetFile:"$FILE" \
      /SourceServerName:"$SERVER" \
      /SourceDatabaseName:"$DB" \
      /p:IgnorePermissions=true \
      /p:IgnoreUserLoginMappings=true
  done
done
```

---

### 3. Config MCP pronta (clientes comuns)

**VS Code / Cursor / Windsurf** (`.vscode/mcp.json` ou settings):

```json
{
  "mcpServers": {
    "sql-mcp": {
      "command": "dab",
      "args": [
        "start",
        "--mcp-stdio",
        "--config",
        "${workspaceFolder}/dab-config.json"
      ],
      "env": {
        "MSSQL_CONNECTION_STRING": "Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
      }
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sql-mcp": {
      "command": "dab",
      "args": ["start", "--mcp-stdio", "--config", "C:\\caminho\\dab-config.json"],
      "env": {
        "MSSQL_CONNECTION_STRING": "Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
      }
    }
  }
}
```

**Versão comunitária simples (Python, read-only):**

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["--from", "microsoft-sql-server-mcp", "mssql_mcp_server"],
      "env": {
        "MSSQL_SERVER": "localhost",
        "MSSQL_DATABASE": "MeuBanco",
        "MSSQL_USER": "usuario",
        "MSSQL_PASSWORD": "senha"
      }
    }
  }
}
```

---

Me diz qual desses você quer aprofundar ou adaptar:

1. Ajustar o `dab-config.json` pro seu banco real (me manda nomes de tabelas/procedures)
2. Script de extração com autenticação Windows / Entra ID
3. Config específica pro Cursor, Claude Desktop ou VS Code
4. Docker Compose do SQL MCP Server

Qual prioridade?

## Referências informadas

Nenhuma referência informada.

## Captura bruta da Issue

<details>
<summary>Exibir corpo original</summary>

**Resumo direto:**

### 1. Ferramentas MCP para SQL Server

#### Oficial da Microsoft (recomendada para produção)
**SQL MCP Server** (parte do **Data API builder / DAB** a partir da versão 1.7/2.0).

- Não expõe SQL livre (mais seguro).
- Trabalha com **entidades** (tabelas, views, procedures) configuradas em JSON.
- Ferramentas principais: `describe_entities`, `read_records`, `create_record`, `update_record`, `delete_record`, `execute_entity`, `aggregate_records`.
- Suporte a RBAC, cache, telemetria, Entra ID etc.
- Documentação: [learn.microsoft.com/sql/mcp](https://learn.microsoft.com/en-us/sql/mcp/) e Data API builder MCP.

Instalação rápida do CLI:

```bash
dotnet tool install -g microsoft.dataapibuilder
dab init --database-type mssql --connection-string "sua-connection-string" --config dab-config.json
dab add MinhaTabela --source dbo.MinhaTabela --permissions "anonymous:read"
dab start --mcp-stdio
```

#### Comunidade (mais simples, geralmente read-only)

| Projeto | Linguagem | Destaque | Stars aprox. |
|---------|-----------|----------|--------------|
| [RichardHan/mssql_mcp_server](https://github.com/RichardHan/mssql_mcp_server) | Python | Mais popular, read-only por padrão, suporta SQL/Windows/Azure AD | ~400 |
| [bilims/mcp-sqlserver](https://github.com/bilims/mcp-sqlserver) | Node.js | Schema discovery + SELECT seguro | ~46 |
| [jdlemes/MsSqlMCP](https://github.com/jdlemes/MsSqlMCP) | .NET | Schema + queries read-only | - |
| [ian-cowley/MCPSqlServer](https://github.com/ian-cowley/MCPSqlServer) | .NET | Schema + execução de SP | - |
| [ConnorBritain/mssql-mcp-server](https://github.com/ConnorBritain/mssql-mcp-server) | Node.js | Versões reader/writer/admin | - |

Exemplo de config (Claude Desktop / Cursor / etc.) para o mais popular:

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["--from", "microsoft-sql-server-mcp", "mssql_mcp_server"],
      "env": {
        "MSSQL_SERVER": "localhost",
        "MSSQL_DATABASE": "seu_banco",
        "MSSQL_USER": "usuario",
        "MSSQL_PASSWORD": "senha"
      }
    }
  }
}
```

---

### 2. CLI para extrair DACPAC

A ferramenta oficial é o **SqlPackage**.

#### Instalação (recomendada)

```bash
dotnet tool install -g microsoft.sqlpackage
```

(Alternativas: download ZIP standalone no site da Microsoft ou via dbatools no PowerShell.)

#### Extrair DACPAC (schema only – padrão)

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco.dacpac \
  /SourceServerName:localhost \
  /SourceDatabaseName:MeuBanco \
  /SourceUser:usuario \
  /SourcePassword:senha
```

#### Com connection string

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco.dacpac \
  /SourceConnectionString:"Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
```

#### Incluir dados de todas as tabelas

```bash
sqlpackage /Action:Extract \
  /TargetFile:MeuBanco_com_dados.dacpac \
  /SourceServerName:localhost \
  /SourceDatabaseName:MeuBanco \
  /p:ExtractAllTableData=true
```

#### Propriedades úteis comuns

| Propriedade | Uso |
|-------------|-----|
| `/p:ExtractAllTableData=true` | Inclui dados de todas as tabelas |
| `/p:IgnorePermissions=true` | Ignora permissões (padrão na maioria dos casos) |
| `/p:IgnoreUserLoginMappings=true` | Ignora mapeamento de logins |
| `/p:VerifyExtraction=true` | Valida o modelo após extração |
| `/p:ExtractTarget=SqlProject` | Extrai como projeto `.sqlproj` em vez de `.dacpac` |

---

### Alternativa PowerShell (dbatools)

```powershell
Install-Module dbatools -Force
Export-DbaDacPackage -SqlInstance "localhost" -Database "MeuBanco" -FilePath "C:\temp\MeuBanco.dacpac"
```

---

**Recomendação prática:**

- Para **agente de IA em produção** → use o **SQL MCP Server oficial** (Data API builder).
- Para exploração rápida de schema + queries → qualquer MCP comunitário read-only.
- Para extrair DACPAC de forma confiável → **SqlPackage** (`dotnet tool`).

Quer que eu monte o `dab-config.json` completo, um script de extração automatizada de vários bancos, ou a config MCP específica para o seu cliente (Cursor, Claude, VS Code etc.)?



Sim. Vou te entregar os três modelos prontos pra usar.

---

### 1. `dab-config.json` completo (SQL MCP Server oficial)

Arquivo de exemplo com tabelas + stored procedure:

```json
{
  "$schema": "https://github.com/Azure/data-api-builder/releases/latest/download/dab.draft.schema.json",
  "data-source": {
    "database-type": "mssql",
    "connection-string": "@env('MSSQL_CONNECTION_STRING')",
    "options": {
      "set-session-context": true
    }
  },
  "runtime": {
    "rest": {
      "enabled": true,
      "path": "/api"
    },
    "graphql": {
      "enabled": true,
      "path": "/graphql"
    },
    "mcp": {
      "enabled": true
    },
    "host": {
      "mode": "development",
      "cors": {
        "origins": ["*"],
        "allow-credentials": false
      },
      "authentication": {
        "provider": "AppService"
      }
    }
  },
  "entities": {
    "Clientes": {
      "source": {
        "object": "dbo.Clientes",
        "type": "table"
      },
      "permissions": [
        {
          "role": "anonymous",
          "actions": ["read"]
        },
        {
          "role": "authenticated",
          "actions": ["create", "read", "update", "delete"]
        }
      ],
      "description": "Cadastro de clientes"
    },
    "Pedidos": {
      "source": {
        "object": "dbo.Pedidos",
        "type": "table"
      },
      "permissions": [
        {
          "role": "authenticated",
          "actions": ["create", "read", "update"]
        }
      ],
      "relationships": {
        "Cliente": {
          "cardinality": "one",
          "target.entity": "Clientes",
          "source.fields": ["ClienteId"],
          "target.fields": ["Id"]
        }
      }
    },
    "ObterPedidoPorId": {
      "source": {
        "object": "dbo.usp_ObterPedidoPorId",
        "type": "stored-procedure"
      },
      "permissions": [
        {
          "role": "authenticated",
          "actions": ["execute"]
        }
      ],
      "mcp": {
        "custom-tool": true
      },
      "description": "Retorna pedido completo por ID"
    }
  }
}
```

**Como subir:**

```bash
# Define a connection string
export MSSQL_CONNECTION_STRING="Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"

# Sobe o MCP em modo stdio (pra Cursor/Claude/VS Code)
dab start --mcp-stdio --config dab-config.json
```

---

### 2. Script de extração de DACPAC (vários bancos)

**PowerShell (Windows / dbatools ou SqlPackage):**

```powershell
# Instala se necessário
# Install-Module dbatools -Force
# dotnet tool install -g microsoft.sqlpackage

$servers = @(
    @{ Server = "localhost"; Databases = @("Banco1", "Banco2", "Banco3") }
    # @{ Server = "outro-servidor"; Databases = @("BancoX") }
)

$outputDir = "C:\Dacpacs\$(Get-Date -Format 'yyyy-MM-dd')"
New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

foreach ($srv in $servers) {
    foreach ($db in $srv.Databases) {
        $file = Join-Path $outputDir "$($srv.Server.Replace('\','_'))_$db.dacpac"
        
        Write-Host "Extraindo $db de $($srv.Server) -> $file"
        
        # Opção 1: SqlPackage
        sqlpackage /Action:Extract `
            /TargetFile:"$file" `
            /SourceServerName:"$($srv.Server)" `
            /SourceDatabaseName:"$db" `
            /p:IgnorePermissions=true `
            /p:IgnoreUserLoginMappings=true `
            /p:ExtractAllTableData=false
        
        # Opção 2: dbatools (alternativa)
        # Export-DbaDacPackage -SqlInstance $srv.Server -Database $db -FilePath $file
    }
}

Write-Host "Concluído. Arquivos em: $outputDir"
```

**Bash (Linux/macOS + SqlPackage):**

```bash
#!/bin/bash
OUTPUT_DIR="./dacpacs/$(date +%Y-%m-%d)"
mkdir -p "$OUTPUT_DIR"

SERVERS=(
  "localhost:Banco1 Banco2 Banco3"
  # "outro-servidor:BancoX"
)

for entry in "${SERVERS[@]}"; do
  SERVER="${entry%%:*}"
  DBS="${entry#*:}"
  
  for DB in $DBS; do
    FILE="$OUTPUT_DIR/${SERVER}_${DB}.dacpac"
    echo "Extraindo $DB de $SERVER -> $FILE"
    
    sqlpackage /Action:Extract \
      /TargetFile:"$FILE" \
      /SourceServerName:"$SERVER" \
      /SourceDatabaseName:"$DB" \
      /p:IgnorePermissions=true \
      /p:IgnoreUserLoginMappings=true
  done
done
```

---

### 3. Config MCP pronta (clientes comuns)

**VS Code / Cursor / Windsurf** (`.vscode/mcp.json` ou settings):

```json
{
  "mcpServers": {
    "sql-mcp": {
      "command": "dab",
      "args": [
        "start",
        "--mcp-stdio",
        "--config",
        "${workspaceFolder}/dab-config.json"
      ],
      "env": {
        "MSSQL_CONNECTION_STRING": "Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
      }
    }
  }
}
```

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sql-mcp": {
      "command": "dab",
      "args": ["start", "--mcp-stdio", "--config", "C:\\caminho\\dab-config.json"],
      "env": {
        "MSSQL_CONNECTION_STRING": "Server=localhost;Database=MeuBanco;User Id=usuario;Password=senha;TrustServerCertificate=True"
      }
    }
  }
}
```

**Versão comunitária simples (Python, read-only):**

```json
{
  "mcpServers": {
    "mssql": {
      "command": "uvx",
      "args": ["--from", "microsoft-sql-server-mcp", "mssql_mcp_server"],
      "env": {
        "MSSQL_SERVER": "localhost",
        "MSSQL_DATABASE": "MeuBanco",
        "MSSQL_USER": "usuario",
        "MSSQL_PASSWORD": "senha"
      }
    }
  }
}
```

---

Me diz qual desses você quer aprofundar ou adaptar:

1. Ajustar o `dab-config.json` pro seu banco real (me manda nomes de tabelas/procedures)
2. Script de extração com autenticação Windows / Entra ID
3. Config específica pro Cursor, Claude Desktop ou VS Code
4. Docker Compose do SQL MCP Server

Qual prioridade?

</details>
