Name:           libmad
Version:        0.15.1b
Release:        1%{?dist}
Summary:        MPEG Audio Decoder

License:        GPLv2
URL:            http://www.underbit.com/products/mad/
Source0:        ftp://ftp.mars.org/pub/mpeg/libmad-%{version}.tar.gz
Patch0:         libmad-0.15.1b-drop-fforce-mem.patch

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
MAD is a high-quality MPEG audio decoder. It currently supports MPEG-1 and the
MPEG-2 extension to lower sampling frequencies, as well as the de facto MPEG
2.5 format. All three audio layers — Layer I, Layer II, and Layer III (i.e.
MP3) — are fully implemented.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1


%build
touch NEWS AUTHORS ChangeLog
autoreconf -fvi
%configure \
	--disable-static \
%if 0%{?__isa_bits} == 64
	--enable-fpm=64bit \
%endif
	--enable-accuracy \
	--disable-debugging
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Create an additional pkgconfig file (borrowed from the RPM Fusion spec)
%{__cat} << EOF > mad.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: mad
Description: MPEG Audio Decoder
Requires:
Version: %{version}
Libs: -L%{_libdir} -lmad -lm
Cflags: -I%{_includedir}
EOF
%{__install} -D -p -m 0644 mad.pc %{buildroot}%{_libdir}/pkgconfig/mad.pc


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license COPYING
%doc CHANGES COPYRIGHT CREDITS README TODO
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun May 15 2016 Jajauma's Packages <jajauma@yandex.ru> - 0.15.1b-1
- Public release
