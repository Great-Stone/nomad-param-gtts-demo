job "gtts-param" {
  datacenters = ["dc1"] # 사용할 데이터 센터 이름으로 수정

  type = "batch" # 배치 작업 유형

  parameterized {
    payload       = "required"
    meta_required = []
  }

  group "create-and-play" {

    network {
      port "player" {}
    }

    task "create" {
      driver = "raw_exec"

      lifecycle {
        hook = "prestart"
        sidecar = false
      }

      config {
        command = "local/start.sh"
      }

      template {
        destination = "local/start.sh"
        data        = <<-EOF
        #!/bin/bash
        echo ${NOMAD_ALLOC_DIR}
        cd local/creator
        pip3 install -r requirements.txt --break-system-packages
        python3 main.py
        EOF
      }

      artifact {
        source      = "https://github.com/Great-Stone/nomad-param-gtts-demo/releases/download/0.1.4/creator.zip"
        destination = "local"
      }

      dispatch_payload {
        file = "../../alloc/conversation.txt"
      }

      resources {
        cpu    = 1
        memory = 256
      }
    }

    task "player" {
      driver = "raw_exec" # 외부 스크립트를 실행

      config {
        command = "local/start.sh"
      }

      env {
        MY_PORT = "${NOMAD_PORT_player}"
      }

      template {
        destination = "local/start.sh"
        data        = <<-EOF
        #!/bin/bash
        cd local/player
        pip3 install -r requirements.txt --break-system-packages
        python3 main.py
        EOF
      }

      artifact {
        source      = "https://github.com/Great-Stone/nomad-param-gtts-demo/releases/download/0.1.4/player.zip"
        destination = "local"
      }

      resources {
        cpu    = 1
        memory = 256
      }
    }
  }
}
