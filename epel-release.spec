Name:           epel-release
Version:        10
Release:        %autorelease
Summary:        Extra Packages for Enterprise Linux repository configuration
# Most things in this package are not considered copyrightable.  If that were
# true for everything in the package, the license identifier would be
# LicenseRef-Not-Copyrightable.  However, the exception is the crb script,
# which is GPL-2.0-only.  Per advice from Fedora Legal, we should use
# GPL-2.0-only as the license identifier for the package in this scenario.
# https://bugzilla.redhat.com/show_bug.cgi?id=2302438
License:        GPL-2.0-only
BuildArch:      noarch
URL:            https://epel.io

# keys
Source10:       https://download.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-%{version}

# repo configs
Source20:       epel.repo
Source21:       epel-testing.repo

# preset policy
Source30:       90-epel.preset

# Add epel crb script
Source31:      crb
# epel crb script is licensed GPL-2.0-only
Source32:      GPL-2.0-only.txt

# The setup process for EPEL involves installing epel-release before the EPEL
# repository is available.  For this to continue to work correctly, all
# dependencies of this package must be available from the default repositories.
# Notably, if weak dependencies of this package are not present at the time of
# installation, they will be skipped and never get installed.
# https://pagure.io/epel/issue/328

# This should only be installed on Enterprise Linux with the same major version
Requires:       (redhat-release >= %{version} with redhat-release < %[%{version} + 1])

# crb needs config-manager to run
# But only recommend it, incase people do not need crb
Recommends:     dnf-command(config-manager)

# SELinux policy modules related to EPEL
Recommends:     (selinux-policy-extra if selinux-policy)


%description
This package contains the Extra Packages for Enterprise Linux (EPEL) repository
configuration and GPG key.

%prep
%setup -q -c -T
# Add epel crb script license
install -pm 644 %{SOURCE32} .


%install
# keys
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/pki/rpm-gpg %{S:10}

# repo configs
install -Dp -m 0644 -t %{buildroot}%{_sysconfdir}/yum.repos.d %{S:20} %{S:21}

# preset policy
install -Dp -m 0644 -t %{buildroot}%{_prefix}/lib/systemd/system-preset %{S:30}

# Add epel crb script
install -D -pm744 -t %{buildroot}%{_bindir} %{SOURCE31}


%post
# Doing a check to see if crb is enabled is as hard and resource intense as enabling or disabling crb.
#   So we will say crb is recommended, without first checking.  But only on the initial install.
if [ "$1" -eq 1 ] ; then
  echo "Many EPEL packages require the CodeReady Builder (CRB) repository."
  echo "It is recommended that you run %{_bindir}/crb enable to enable the CRB repository."
fi


%files
%license GPL-2.0-only.txt
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-EPEL-%{version}
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel.repo
%config(noreplace) %{_sysconfdir}/yum.repos.d/epel-testing.repo
%{_prefix}/lib/systemd/system-preset/90-epel.preset
%{_bindir}/crb


%changelog
%autochangelog
