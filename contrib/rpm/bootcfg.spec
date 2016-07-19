%global import_path github.com/coreos/coreos-baremetal
%global repo coreos-baremetal

Name:	    bootcfg
Version:	0.3.0
Release:	1%{?dist}
Summary:	Machine boot and provision server
License:	ASL 2.0
URL:		https://%{import_path}
Source0:	https://%{import_path}/archive/v%{version}.tar.gz

# Limit to architectures supported by golang or gcc-go compilers
ExclusiveArch: %{go_arches}
# Use golang or gcc-go compiler depending on architecture
BuildRequires: compiler(go-compiler)

%description
bootcfg is an HTTP and gRPC server that renders Ignition configs,
cloud-configs, iPXE/GRUB network boot configs, and meta-data to boot and
provision clusters of CoreOS machines. Configs can be templated and
optionally GPG signed.

%prep
# Tarball has <repo>-<version> top level dir, not <name>-<version>
%setup -q -n %{repo}-%{version}

%build
# create a Go workspace with a symlink to builddir source
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/coreos-baremetal
export GOPATH=$(pwd):%{gopath}
%gobuild -o bin/bootcfg %{import_path}/cmd/bootcfg

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sharedstatedir}/%{name}
install -p -m 0755 bin/bootcfg %{buildroot}%{_bindir}

%files
%doc README.md CHANGES.md CONTRIBUTING.md LICENSE NOTICE DCO
%{_bindir}/bootcfg
%{_sharedstatedir}/%{name}

%changelog
* Mon Jul 11 2016 Initial package <dalton.hubble@coreos.com> - 0.3.0-1
- Initial package

