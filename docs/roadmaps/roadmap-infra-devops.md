# Roadmap de Infraestrutura & DevOps

**Projeto:** sistema de finanças pessoais (veículo de aprendizado)
**Foco deste documento:** **só infra e DevOps** — não a aplicação em si.
**Princípio central:** sobe uma versão simples **ponta a ponta no ar logo**, e a **infra cresce em níveis**. Cada nível é um checkpoint: marque conforme avança. O que torna os experimentos caros seguros é **descrever tudo em código (IaC)** — sobe com um comando, destrói com outro.

> Como usar: faça os níveis em ordem. Os Níveis 0–2 ficam **no ar** como seu ambiente fixo. Os Níveis 3–5 podem ser **efêmeros** (sobe, experimenta, destrói) — ótimos pra continuar como estudo de fim de semana mesmo depois de empregado.
> Os nomes em **negrito** estão explicados no **Glossário** no fim.

---

## Nível 0 — v1 no ar, de graça, com higiene mínima

**Objetivo:** ter o sistema funcionando publicamente em 1–2 semanas, mesmo que faça quase nada — mas já com boas práticas básicas.

- Código no Git com **branch protection** na `main`.
- App **dockerizado**: **Dockerfile** **multi-stage**, rodando como usuário não-root, versões pinadas.
- **docker-compose** local (app + banco) pra subir tudo com um comando.
- Primeira **pipeline de CI/CD** no **GitHub Actions**: em PR roda lint + testes; no merge, builda e faz deploy.
- Config por **variável de ambiente** (princípio **12-factor**); segredos nos secrets da plataforma, nunca no código.
- Health check, **log estruturado** (JSON), readiness/liveness.
- Deploy: back-end no **Render** (ou **Railway**); front-end na **Vercel** (ou **Cloudflare Pages**); banco no **Supabase**.

**Aprende:** o loop de deploy, autoria de pipeline, containerização, 12-factor.
**Custo:** R$0.
**Modo:** manter no ar.

---

## Nível 1 — dono do artefato e dos controles de qualidade

**Objetivo:** separar build de deploy e adicionar barreiras de qualidade/segurança.

- CI builda a imagem e dá push num **container registry** (**GHCR**, grátis em repo público); o deploy puxa a imagem versionada.
- Barreiras de qualidade: **coverage gate**, scan de vulnerabilidade com **Trivy**, análise estática com **SonarCloud**.
- **Migrations** de banco na pipeline (**Alembic**, no caso de Python).
- Ambientes separados: **staging** e **produção** (preview por PR na Vercel).
- Segredos de verdade: **Doppler** ou **SOPS**.
- Observabilidade básica: logs + métricas num free tier (**New Relic** ou **Grafana Cloud**), um **uptime check** e um **alerta**.

**Aprende:** cadeia de artefatos, segurança de supply chain, promoção de ambientes, gestão de segredos, observabilidade.
**Custo:** ~R$0.
**Modo:** manter no ar.

---

## Nível 2 — você vira o "ops": um servidor que é seu

**Objetivo:** aprender o que o PaaS esconde, administrando um servidor na unha.

- Um **VPS** baratinho (**Hetzner** ~€4/mês ou **DigitalOcean Droplet**).
- Acesso por **SSH**, **firewall** (ufw), usuário de deploy não-root.
- **Reverse proxy** + **TLS** automático com **Caddy** (ou nginx/Traefik) — HTTPS via **Let's Encrypt**.
- App rodando via docker-compose na máquina; deploy via GitHub Actions por SSH.
- **systemd** pra manter processos vivos, rotação de log, **backup** agendado (**cron** + pg_dump pra um storage).
- Um domínio próprio (uns poucos dólares/ano) → DNS e HTTPS reais.

**Aprende:** Linux ops, rede, TLS, proxy reverso, backup — o trabalho do time de plataforma das empresas.
**Custo:** ~US$4–6/mês.
**Modo:** manter no ar (vira seu "prod").

---

## Nível 3 — Kubernetes de verdade, mas local e de graça

**Objetivo:** ficar fluente em **Kubernetes** sem gastar nada.

- Suba um cluster local com **kind**, **k3d** ou **minikube**.
- Traduza o app pros objetos do k8s: **Deployment**, **Service**, **Ingress**, **ConfigMap**/**Secret**, **probes** de liveness/readiness, **requests/limits** de recurso, **HPA**, **namespaces**.
- Empacote o app com **Helm** (um **chart**).
- Instrumente com **OpenTelemetry** e visualize com **Prometheus + Grafana** rodando no próprio cluster.

**Aprende:** o modelo mental do k8s e Helm, mais observabilidade hands-on — tudo sem fatura.
**Custo:** R$0.
**Modo:** local (liga/desliga à vontade).

---

## Nível 4 — Infraestrutura como Código (o destravador)

**Objetivo:** descrever a infra em código pra poder recriá-la e apagá-la com um comando.

- **Terraform** (ou **OpenTofu**): codifique o VPS do Nível 2 e, depois, os recursos de cloud.
- `terraform apply` cria tudo; `terraform destroy` apaga tudo.
- **Remote state** (Terraform Cloud free pra começar).
- (Opcional) **Ansible** pra configurar o servidor.

**Aprende:** IaC, reprodutibilidade e o fluxo "sobe/destrói" que torna o Nível 5 seguro.
**Custo:** ~R$0 (a ferramenta é grátis).
**Modo:** base pros experimentos.

---

## Nível 5 — a "prévia de empresa grande", efêmera

**Objetivo:** montar uma stack realista de empresa numa cloud real, viver a experiência por horas e destruir.

Componentes que deixam "cara de produção": k8s gerenciado, banco gerenciado, **ingress controller** + **cert-manager** (TLS), **kube-prometheus-stack** (Prometheus + Grafana), **ArgoCD** (**GitOps**) e **Argo Rollouts** (**canary**), **container registry** da cloud.

Onde rodar (escolha por experimento):
- **Mais barato e portável:** **GKE** (GCP) — fee de cluster coberto pelo crédito grátis de ~US$74,40/mês + US$300 de bônus na conta nova. Melhor pra deixar de pé por uns dias.
- **Mais "keyword de currículo":** **AWS EKS** — o mais caro (control plane US$0,10/h) e cheio de pegadinha; use por horas e destrua.
- **Simples e travado na AWS:** **ECS + Fargate** — control plane grátis, sem gerenciar nós; bom pra sentir o contraste com k8s.
- **Multi-cloud (opcional, alto valor):** rode o **mesmo Helm chart** no EKS e depois no GKE, trocando só o provider do Terraform — é assim que se aprende a ser agnóstico de cloud.

Experiências pontuais que valem o nome no currículo:
- **CI/CD no Jenkins** uma vez (self-hosted em container, com **Jenkinsfile**) — comum em banco/fintech.
- **APM no Datadog** via trial de 14 dias (instalar o agente e instrumentar você mesmo).
- Segredos no **HashiCorp Vault** (self-hosted) e/ou **AWS Secrets Manager**, puxados pro cluster via **External Secrets Operator**.

**Aprende:** k8s gerenciado, GitOps, canary, TLS automático, observabilidade e segredos "de empresa", multi-cloud.
**Custo:** alguns dólares por experimento, sob seu controle.
**Modo:** efêmero (sobe → experimenta → destrói).

---

## Regras anti-susto de custo (decore antes de mexer em cloud paga)

1. **Alarme de billing + Budget** (ex.: US$10) **antes** do primeiro `apply`.
2. **Evite o NAT Gateway** em cluster de estudo — é o custo silencioso nº 1 (~US$33/mês mesmo parado).
3. **EKS:** pine a versão do Kubernetes numa de suporte padrão (o "extended support" pula de US$0,10 pra US$0,60/h).
4. Depois do `terraform destroy`, **varra o console à mão**: load balancers, volumes (EBS/PV) e IPs públicos/Elastic IPs costumam ficar pra trás cobrando.
5. Para EKS, prefira **sessões de horas + destruir**; para algo de pé por dias, use **GKE** ou k8s gerenciado de control plane grátis (**DOKS/Civo/Linode**).

---

## Glossário — o que é / pra que serve

### Hospedagem e deploy
- **PaaS** — "plataforma como serviço": você entrega o código e ela cuida de servidor, rede e deploy por você.
- **Render** — PaaS pra **back-end**: recebe seu código/container, sobe, te dá uma URL e oferece banco gerenciado. (Free tier "dorme" quando ocioso e leva ~1 min pra acordar.)
- **Railway** — PaaS parecido com o Render, deploy direto do Git; dá ~US$5/mês de crédito grátis.
- **Vercel** — hospedagem de **front-end**: a cada push no Git, faz o build do site e serve numa **CDN** global com HTTPS. Free tier (Hobby) generoso.
- **Cloudflare Pages** — hospedagem de front-end na CDN da Cloudflare; banda ilimitada no grátis.
- **Netlify** — alternativa à Vercel pra front-end.
- **Supabase** — Postgres gerenciado + autenticação + storage, com free tier.
- **CDN** — rede de servidores espalhados pelo mundo que entrega arquivos estáticos rapidinho perto de cada usuário.

### Containers
- **Docker** — empacota o app + tudo que ele precisa num "container" que roda igual em qualquer lugar.
- **Dockerfile** — a receita de como construir a imagem do container.
- **Multi-stage build** — técnica de Dockerfile que deixa a imagem final menor e mais segura.
- **docker-compose** — sobe vários containers juntos (ex.: app + banco) localmente com um comando.
- **Container registry** (**GHCR**, **ECR**, **Artifact Registry**) — a "prateleira" onde ficam as imagens prontas pra deploy.

### CI/CD
- **CI/CD** — esteira automática que testa, builda e publica seu código a cada mudança.
- **GitHub Actions** — ferramenta de CI/CD integrada ao GitHub; grátis em repositório público.
- **Jenkins** — servidor de CI/CD clássico, auto-hospedado; ainda muito usado em empresa grande/banco.
- **Jenkinsfile** — arquivo que descreve a pipeline no Jenkins.
- **Branch protection** — regra que impede mexer direto na `main` sem revisão/testes passando.

### Qualidade e segurança no pipeline
- **Trivy** — scanner que procura vulnerabilidades conhecidas na imagem do container.
- **SonarQube / SonarCloud** — análise estática de qualidade e segurança do código.
- **Coverage gate** — barreira que reprova o build se a cobertura de testes cair abaixo de um limite.
- **Alembic** — ferramenta de **migrations** (versiona mudanças no schema do banco) no mundo Python.
- **Migration** — uma mudança versionada e reversível na estrutura do banco de dados.

### Configuração e segredos
- **12-factor** — conjunto de boas práticas pra apps de nuvem; a mais famosa é "config vem de variável de ambiente, não do código".
- **Variável de ambiente** — configuração injetada de fora, separada do código.
- **Doppler** — serviço que centraliza segredos/config e injeta nas suas apps.
- **SOPS** — criptografa segredos pra você poder guardá-los no Git com segurança.
- **HashiCorp Vault** — servidor dedicado de segredos, com rotação automática, segredos temporários e políticas de acesso finas; padrão em empresa regulada.
- **AWS Secrets Manager / GCP Secret Manager** — cofres de segredos gerenciados das respectivas clouds.
- **External Secrets Operator** — leva os segredos do cofre pra dentro do Kubernetes automaticamente.
- **Sealed Secrets** — outra forma de guardar segredos criptografados no Git pro k8s.

### Servidor próprio (VPS)
- **VPS** — um servidor Linux virtual só seu, onde você administra tudo.
- **Hetzner / DigitalOcean Droplet** — provedores de VPS baratos.
- **SSH** — acesso remoto seguro ao servidor, via terminal.
- **Firewall (ufw)** — controla quais portas/conexões podem entrar.
- **Reverse proxy** — recebe o tráfego da internet e direciona pro serviço certo; também cuida do HTTPS.
- **Caddy / nginx / Traefik** — programas que fazem esse papel de reverse proxy.
- **TLS / Let's Encrypt** — TLS é o que faz o "cadeado" (HTTPS); Let's Encrypt emite o certificado de graça.
- **systemd** — gerenciador de serviços do Linux; reinicia o processo se ele cair.
- **Cron** — agendador de tarefas (ex.: backup todo dia às 3h).

### Kubernetes
- **Kubernetes (k8s)** — orquestrador que roda e gerencia containers em escala: mantém réplicas no ar, reinicia o que falha, distribui carga.
- **kind / k3d / minikube** — Kubernetes rodando na sua máquina, de graça, pra aprender.
- **Deployment** — objeto que mantém N cópias (réplicas) do seu app no ar.
- **Service** — dá um endereço estável pros containers se acharem e conversarem.
- **Ingress / Ingress controller** — o "porteiro" HTTP que recebe o tráfego externo e roteia pros serviços.
- **ConfigMap / Secret** — onde ficam config e segredos dentro do cluster.
- **Liveness / readiness probes** — checagens de saúde que dizem se o container está vivo e pronto pra receber tráfego.
- **HPA (Horizontal Pod Autoscaler)** — sobe e desce o número de réplicas conforme a carga.
- **Namespace** — uma "pasta" lógica pra separar ambientes/recursos no cluster.
- **Helm / chart** — o "gerenciador de pacotes" do k8s; o chart é o pacote parametrizável do seu app.
- **cert-manager** — emite e renova certificados TLS automaticamente dentro do k8s.

### Clouds e orquestração gerenciada
- **AWS EKS** — Kubernetes gerenciado da AWS (control plane ~US$73/mês).
- **GCP GKE** — Kubernetes gerenciado do Google; a taxa de cluster costuma ser coberta por crédito grátis mensal.
- **Azure AKS** — equivalente da Microsoft.
- **DigitalOcean DOKS / Civo / Linode LKE** — k8s gerenciado barato, com control plane grátis (paga só os nós).
- **ECS** — orquestrador de containers proprietário da AWS; control plane grátis, mas te prende na AWS.
- **Fargate** — modo "serverless" de container: você roda containers sem gerenciar máquinas/nós.
- **NAT Gateway** — componente de rede que deixa recursos privados acessarem a internet; cobra por hora (pegadinha de custo).
- **Load Balancer (ALB)** — distribui o tráfego entre as réplicas do app.
- **EBS / Persistent Volume** — disco persistente que sobrevive ao reinício do container.
- **Elastic IP** — IP fixo na cloud (cobra mesmo quando ocioso).

### Infraestrutura como Código (IaC)
- **IaC** — descrever a infraestrutura em arquivos de código, versionáveis e reproduzíveis.
- **Terraform / OpenTofu** — a ferramenta de IaC; `apply` cria os recursos, `destroy` apaga.
- **Remote state** — onde o Terraform guarda o "mapa" do que já criou.
- **Ansible** — automatiza a configuração de servidores (instalar pacotes, ajustar arquivos).

### Entrega contínua / GitOps
- **GitOps** — o repositório Git vira a "fonte da verdade" do deploy; uma ferramenta sincroniza o cluster com o que está no Git.
- **ArgoCD** — a ferramenta que faz GitOps (observa o Git e aplica no cluster).
- **Argo Rollouts** — faz deploy progressivo.
- **Canary deployment** — sobe a versão nova pra uma fração dos usuários, observa, e só então libera pra 100%.

### Observabilidade
- **Observabilidade** — conseguir enxergar o que o sistema está fazendo por dentro.
- **Logs** — o diário de texto dos eventos ("erro ao salvar X").
- **Métricas** — números ao longo do tempo (CPU, requisições/s, latência); viram gráficos de tendência.
- **Traces / APM** — seguir **uma** requisição atravessando os serviços e ver onde demorou (o "raio-X" da request).
- **Alertas** — avisos disparados quando um número passa de um limite.
- **Dashboards** — painéis que reúnem os gráficos.
- **Uptime / synthetics** — um robô externo checando se o sistema está no ar.
- **Prometheus** — coleta e armazena métricas.
- **Grafana** — monta dashboards e dispara alertas (em cima do Prometheus, por exemplo).
- **Loki** — armazena e busca logs (ecossistema Grafana).
- **Tempo / Jaeger** — armazenam e exibem traces.
- **kube-prometheus-stack** — pacote pronto que instala Prometheus + Grafana + dashboards no cluster de uma vez.
- **OpenTelemetry (OTel)** — padrão neutro de instrumentação: você instrumenta o app uma vez e manda os dados pra qualquer ferramenta (Datadog, New Relic, Grafana...).
- **Datadog** — plataforma SaaS paga all-in-one de observabilidade (free tier limitado, sem APM; APM no trial).
- **New Relic** — concorrente do Datadog com free tier generoso (100GB/mês), bom pra aprender APM de graça.
- **Sentry** — rastreia e agrupa erros/exceções do código.
- **Billing alarm / Budget** — alarme de custo configurado na cloud pra te avisar (ou cortar) antes da conta crescer.
