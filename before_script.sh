if [[ -v "GL_TOKEN" || -v "GITLAB_TOKEN" ]]; then
  if [[ "${CI_PROJECT_URL}" =~ (([^/]*/){3}) ]]; then
    mkdir -p $HOME/.config/git
    echo "${BASH_REMATCH[1]/:\/\//://gitlab-ci-token:${GL_TOKEN:-$GITLAB_TOKEN}@}" > $HOME/.config/git/credentials
    git config --global credential.helper store
  fi
fi
