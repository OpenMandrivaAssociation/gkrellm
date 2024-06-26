Name:		gkrellm
Version:	2.3.11
Release:	2
Summary:	Multiple stacked system monitors
License:	GPLv3+
Group:		Monitoring
URL:		https://gkrellm.srcbox.net/
Source0:	https://gkrellm.srcbox.net/releases/gkrellm-%{version}.tar.bz2
#Source0:	http://members.dslextreme.com/users/billw/gkrellm/%{name}-%{version}.tar.bz2
Source1:	gkrellm-themes.tar.bz2
Source2:	gkrellmd.service
Source3:	gkrellm-pt.po
#Patch0:		gkrellm-2.3.5-fix-format-errors.patch
#Patch2:		gkrellm-2.3.5-force-libsensor-test-result.patch
BuildRequires:	gettext
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(libntlm)
BuildRequires:	lm_sensors-devel
BuildRequires:	locales-extra-charsets

%description
GKrellM charts SMP CPU, load, Disk, and all active net interfaces
automatically. An on/off button and online timer for the PPP interface
is provided. Monitors for memory and swap usage, file system, internet
connections, APM laptop battery, mbox style mailboxes, and cpu temps.
Also includes an uptime monitor, a hostname label, and a clock/calendar.
Additional features are:

  * Autoscaling grid lines with configurable grid line resolution.
  * LED indicators for the net interfaces.
  * A gui popup for configuration of chart sizes and resolutions.

THIS PACKAGE IS CONSIDERED DEPRECATED BECAUSE IT HAS BEEN ABANDONED
UPSTREAM. IT MAY BE REMOVED IN A FUTURE RELEASE WITHOUT FURTHER NOTICE.
IT IS RECOMMENDED TO USE AN ALTERNATIVE, SUCH AS plasma6-systemmonitor

%package devel
Summary:	Include files for gkrellm
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
gkrellm header files for gkrellm development and plugin support.

THIS PACKAGE IS CONSIDERED DEPRECATED BECAUSE IT HAS BEEN ABANDONED
UPSTREAM. IT MAY BE REMOVED IN A FUTURE RELEASE WITHOUT FURTHER NOTICE.
IT IS RECOMMENDED TO USE AN ALTERNATIVE, SUCH AS plasma6-systemmonitor

%package server
Summary:	Server component for gkrellm
Group:		Monitoring
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description server
The server component allows you to monitor a server remotely from 
a client running gkrellm, without installing gkrellm on the server.

THIS PACKAGE IS CONSIDERED DEPRECATED BECAUSE IT HAS BEEN ABANDONED
UPSTREAM. IT MAY BE REMOVED IN A FUTURE RELEASE WITHOUT FURTHER NOTICE.
IT IS RECOMMENDED TO USE AN ALTERNATIVE, SUCH AS plasma6-systemmonitor

%prep
%setup -q
%setup -q -D -T -a1
cp -a %{S:3} po/pt.po
for i in `find -type d -name .xvpics`
    do rm -rf $i
done
# make it lib64 aware
perl -pi -e "/PLUGINS_DIR/ and s|/lib/|/%{_lib}/|g" ./src/gkrellm.h ./server/gkrellmd.h
perl -pi -e "s|/lib/|/%{_lib}/|" Makefile
#patch0 -p1 -b .wformat
#patch2 -p1 -b .libsensors

%build
%make INSTALLROOT=%{_prefix} \
      INCLUDEDIR=%{_includedir} \
      CFLAGS="%optflags" \
      LDFLAGS="%ldflags" \
      LOCALEDIR=%{_datadir}/locale

%install
mkdir -p %{buildroot}/%{_bindir}
make install \
    INSTALLROOT=%{buildroot}%{_prefix} \
    INSTALLDIR=%{buildroot}/%{_bindir} \
    INCLUDEDIR=%{buildroot}%{_includedir} \
    MANDIR=%{buildroot}%{_mandir}/man1 \
    LOCALEDIR=%{buildroot}%{_datadir}/locale \
    STRIP=""

mkdir -p %{buildroot}%{_libdir}/%{name}2/plugins

mkdir -p %{buildroot}{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
convert src/icon.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert src/icon.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/icon.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/%{name}2/themes
cp -av gkrellm-themes/* %{buildroot}%{_datadir}/%{name}2/themes

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/%{_real_vendor}-%{name}.desktop << EOF
[Desktop Entry]
Name=Gkrellm
Comment=A GTK-based monitoring app
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;System;Monitor;
EOF

install -D -p -m 0644 server/gkrellmd.conf %{buildroot}%{_sysconfdir}/gkrellmd.conf
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/gkrellmd.service

#multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellm.h
#multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellmd.h

%{find_lang} %{name}

# lock dir
install -d -m 755 %{buildroot}%{_localstatedir}/lock/gkrellm
chmod 1777 %{buildroot}%{_localstatedir}/lock/gkrellm


%files -f %{name}.lang
%doc COPYRIGHT Changelog INSTALL README *.html
%{_bindir}/gkrellm
%{_datadir}/applications/%{_real_vendor}-%{name}.desktop
%{_iconsdir}/gkrellm.png
%{_liconsdir}/gkrellm.png
%{_miconsdir}/gkrellm.png
%{_mandir}/man1/gkrellm.1*
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2/

%files devel
%doc *.html
%{_includedir}/gkrellm2
%{_libdir}/pkgconfig/gkrellm.pc
#multiarch %{_includedir}/multiarch-*/gkrellm2

%files server
%config(noreplace) %{_sysconfdir}/gkrellmd.conf
%{_unitdir}/gkrellmd.service
%{_bindir}/gkrellmd
%{_mandir}/man1/gkrellmd.1*
